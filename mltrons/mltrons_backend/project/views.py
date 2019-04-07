from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.decorators import list_route, detail_route
from datetime import datetime, date
from django.template.loader import render_to_string
import time
import json
import pandas as pd
from django.core.files.storage import FileSystemStorage
from mlbot.algorithms.data_summary import *
from mlbot.algorithms.save_read import *
from django.conf import settings
from .tasks import *
from celery.result import AsyncResult
from django.http import JsonResponse
from mlbot_webservices.celery import app

def get_task_progress(request):
    task_id = request.POST.get('task_id', None)
    if task_id is not None:
        task = AsyncResult(task_id)
        data = {
            'state': task.state,
            'result': task.result,
        }
        context = {'status': True, 'output': data}
    else:
        context = {'status': False, 'message': 'No Task ID provided'}
    return JsonResponse(context)

class ProjectViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin):
    model = Project
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super(ProjectViewSet, self).list(request, *args, **kwargs)
        return Response({'success': True, 'results': response.data})

    def create(self, request, *args, **kwargs):
        project = super(ProjectViewSet, self).create(request, *args, **kwargs)
        return Response({'success': True})

    def retrieve(self, request, *args, **kwargs):
        response = super(ProjectViewSet, self).retrieve(request, *args, **kwargs)
        return Response({'success': True, 'result': response.data})

    def destroy(self, request, *args, **kwargs):
        response = super(ProjectViewSet, self).destroy(request, *args, **kwargs)
        return Response({'success': True})

    @detail_route(methods=['get'], url_path='task')
    def get_task_progress(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('pk', None)
            task = Task.objects.filter(project_id=project_id).exclude(status=Task.Completed).latest('created_at')
            t = AsyncResult(task.task_id)
            result = None
            if t.status != 'PENDING':
                if t.result['step'] == 5 or t.result['step'] == 6:
                    task.status = Task.Completed
                    task.save()
                result = {
                    'state': t.state,
                    'result': t.result,
                }
            else:
                result = {
                    'state': t.state,
                    'result': {'step': 0},
                }

            return Response({'data': result, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'no task found.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)


class TestingModelViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    model = TestingData
    serializer_class = TestingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super(TestingModelViewSet, self).retrieve(request, *args, **kwargs)
        return Response({'success': True, 'result': response.data})

    @detail_route(methods=['get'], url_path='by-dataset')
    def get_testing_by_dataset(self, request, *args, **kwargs):
        try:
            dataset_id = kwargs.get('pk', None)
            trainings = self.model.objects.filter(data_id=dataset_id, status=self.model.Pending)
            data = self.serializer_class(trainings, many=True).data
            return Response({'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Something went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'], url_path='upload')
    def upload_testing_set(self, request, *args, **kwargs):
        try:
            data = request.POST.get('data', None)
            project = request.POST.get('project', None)
            file = request.FILES['file_url']
            if data and file:
                training = self.model.objects.create(data_id=data, file_url=file)
                # process file here
                # change here
                suffix = training.data.suffix
                result = read_and_process_training_csv.delay(training.id, training.file_url.path, request.user.id, suffix)
                print(result)
                Task.objects.create(project_id=project, task_id=result.id, type='test_csv')
                return Response(data={'success': True, 'task_id': result.id}, status=status.HTTP_200_OK)
            else:
                return Response(data={'error': 'Request parameters missing.', 'success': False},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data={'error': 'Something went wrong.', 'success': False},
                            status=status.HTTP_400_BAD_REQUEST)


class DataSetViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    model = DataSet
    serializer_class = DatasetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.filter(project__in=self.request.user.projects.all())

    def retrieve(self, request, *args, **kwargs):
        response = super(DataSetViewSet, self).retrieve(request, *args, **kwargs)
        return Response({'success': True, 'result': response.data})

    def destroy(self, request, *args, **kwargs):
        response = super(DataSetViewSet, self).destroy(request, *args, **kwargs)
        return Response({'success': True})

    @detail_route(methods=['get'], url_path='by-project')
    def get_datasets_by_project(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('pk', None)
            datasets = self.model.objects.filter(project_id=project_id)
            data = self.serializer_class(datasets, many=True).data
            return Response({'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Someting went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'], url_path='update-loc')
    def update_loc(self, request, *args, **kwargs):
        nodes = request.data
        for node in nodes:
            try:
                self.model.objects.filter(id=node['dataset_id']).update(loc=node['loc'])
            except Exception as e:
                pass
        return Response({'success': True}, status=status.HTTP_200_OK)

    @list_route(methods=['post'], url_path='upload')
    def upload_dataset(self, request, *args, **kwargs):
        try:
            project = request.POST.get('project', None)
            file = request.FILES['file_url']
            if project and file:
                dataset = DataSet.objects.create(project_id=project, file_url=file, name=file.name)
                count = DataSet.objects.filter(project_id=project).count()
                # process file here
                # result = read_and_process_csv(dataset.id, dataset.file_url.path, request.user.id, count)
                result = read_and_process_csv.delay(dataset.id, dataset.file_url.path, request.user.id, count)

                print(result, "zhi shi result. wo yao kaam")
                Task.objects.create(project_id=project, task_id=result.id, type='read_csv')
                return Response(data={'success': True, 'task_id': result.id}, status=status.HTTP_200_OK)
            else:
                return Response(data={'error': 'Request parameters missing.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e, "test")
            return Response(data={'error': 'Someting went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'], url_path='data')
    def get_data_by_dataset(self, request, *args, **kwargs):
        try:
            dataset_id = kwargs.get('pk', None)
            limit = self.request.GET.get('limit')
            offset = self.request.GET.get('offset')
            offset = int(offset)
            dataset = self.model.objects.get(id=dataset_id)
            reader = save_read(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
            data = reader.read_parquet_as_json(bucket=settings.S3_BUCKET, path=dataset.frame_path, offset=offset, limit=10)
            return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Someting went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)


class MetaViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    model = Meta
    serializer_class = MetaSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super(MetaViewSet, self).retrieve(request, *args, **kwargs)
        return Response({'success': True, 'result': response.data})

    def update(self, request, *args, **kwargs):
        response = super(MetaViewSet, self).update(request, *args, **kwargs)
        return Response({'success': True, 'result': response.data})

    @detail_route(methods=['get'], url_path='by-dataset')
    def get_metas_by_dataset(self, request, *args, **kwargs):
        try:
            dataset_id = kwargs.get('pk', None)
            metas = self.model.objects.filter(data_id=dataset_id)
            data = self.serializer_class(metas, many=True).data
            return Response(data={'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': 'Someting went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)



class MetaConnectionViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.CreateModelMixin):
    model = MergeColumn
    serializer_class = MergeColumnSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.all()

    def create(self, request, *args, **kwargs):
        response = super(MetaConnectionViewSet, self).create(request, *args, **kwargs)
        return Response({'success': True, 'result': response.data})

    def destroy(self, request, *args, **kwargs):
        response = super(MetaConnectionViewSet, self).destroy(request, *args, **kwargs)
        return Response({'success': True})

    @detail_route(methods=['get'], url_path='by-project')
    def get_meta_connections(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('pk', None)
            metas = self.model.objects.filter(project_id=project_id)
            data = self.serializer_class(metas, many=True).data
            return Response({'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Someting went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='merge')
    def process_meta_connections(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('pk', None)
            self.model.objects.filter(project_id=project_id).delete()
            nodes = request.data
            for node in nodes:
                self.model.objects.create(project_id = project_id, from_column_id = node['from_column'], to_column_id = node['to_column'])

            result = merge_and_process_csv.delay(project_id, request.user.id)
            print(result)
            Task.objects.create(project_id=project_id, task_id=result.id, type='merge_csv')

            return Response(data={'success': True, 'task_id': result.id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Someting went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

class TrainingDetailViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.CreateModelMixin):
    model = TrainingDetail
    serializer_class = TrainingDetailSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print('create here')
        self.model.objects.filter(project_id=request.data['project']).delete()
        response = super(TrainingDetailViewSet, self).create(request, *args, **kwargs)
        data = response.data
        obj = self.model.objects.get(id=data['id'])
        obj.selected_columns = {
            'columns': request.data['selected']
        }
        obj.save()
        result = start_training.delay(obj.id, request.user.id)
        Task.objects.create(project_id=request.data['project'], task_id=result.id, type='train_csv')

        return Response({'success': True, 'task_id': result.id})

    @detail_route(methods=['get'], url_path='by-project')
    def get_training(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('pk', None)
            training = self.model.objects.filter(project_id=project_id)
            data = self.serializer_class(training, many=True).data
            return Response({'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Someting went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'], url_path='interrupt')
    def interrupt_training(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('pk', None)
            # task = Task.objects.filter(project_id=project_id, type='train_csv').exclude(status=Task.Completed).latest('created_at')
            training = self.model.objects.filter(project_id=project_id).latest('id')
            training.interupt = True
            training.save()
            # app.control.revoke(task.task_id)
            # task.project.status = Project.Completed
            # task.project.save()
            # task.status = Task.Completed
            # task.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Someting went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)


class DeployedModellViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.CreateModelMixin):
    model = DeployedModel
    serializer_class = DeployedModelSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        response = super(DeployedModellViewSet, self).create(request, *args, **kwargs)
        return Response({'success': True, 'data': response.data})

    @detail_route(methods=['get'], url_path='by-project')
    def get_deployed_model(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('pk', None)
            deployed_models = self.model.objects.filter(project_id=project_id)
            data = self.serializer_class(deployed_models, many=True).data
            return Response({'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Something went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'], url_path='graph')
    def get_prediction(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('pk', None)
            graph = Graph.objects.filter(project_id=project_id)
            data = GraphSerializer(graph, many=True).data
            return Response({'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Something went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'], url_path='testing')
    def test_deployed_model(self, request, *args, **kwargs):
        try:
            model_id = kwargs.get('pk', None)
            project_id = request.GET.get('project', None)
            # do merging, transformation, graph generation here
            result = start_testing.delay(model_id, request.user.id)
            Task.objects.create(project_id=project_id, task_id=result.id, type='generate_graph_csv')

            return Response({'success': True, 'task_id': result.id})
        except Exception as e:
            return Response({'error': 'Something went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)


class TrainingModelViewSet(viewsets.GenericViewSet):
    model = TrainingModel
    serializer_class = TrainingModelSerializer
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['get'], url_path='by-training')
    def get_training(self, request, *args, **kwargs):
        try:
            training_id = kwargs.get('pk', None)
            models = self.model.objects.filter(training_id=training_id)
            data = self.serializer_class(models, many=True).data
            return Response(data={'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': 'Something went wrong.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'], url_path='by-rank')
    def filter_models(self, request, *args, **kwargs):
        try:
            training_id = kwargs.get('pk', None)
            metric_id = request.GET.get('metric', None)
            models = TrainingModel.objects.filter(training_id=training_id, modelmetric__metric__id=metric_id).order_by('modelmetric__value')
            data = self.serializer_class(models, many=True).data
            return Response(data={'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': 'Something went wrong.', 'success': False},
                            status=status.HTTP_400_BAD_REQUEST)


    @detail_route(methods=['get'], url_path='accuracy')
    def get_accuracy(self, request, *args, **kwargs):
        try:
            model_id = kwargs.get('pk', None)
            project_id = request.GET.get('project', None)
            model = ModelMetric.objects.filter(model_id=model_id)
            data = AccuracySerializer(model, many=True).data
            return Response(data={'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': 'Does not exist', 'success': False}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='roc')
    def get_roc(self, request, *args, **kwargs):
        try:
            model_id = kwargs.get('pk', None)
            project_id = request.GET.get('project', None)
            model = ROC.objects.get(training_model_id=model_id, project_id=project_id)
            data = ROCSerializer(model, many=False).data
            return Response(data={'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': 'Does not exist', 'success': False}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='blue-print')
    def get_blueprint(self, request, *args, **kwargs):
        try:
            model_id = kwargs.get('pk', None)
            project_id = request.GET.get('project', None)
            model = BluePrint.objects.get(training_model_id=model_id, project_id=project_id)
            data = BluePrintSerializer(model, many=False).data
            return Response(data={'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': 'Does not exist', 'success': False}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='feature-importance')
    def get_featureimportance(self, request, *args, **kwargs):
        try:
            model_id = kwargs.get('pk', None)
            project_id = request.GET.get('project', None)
            model = FeatureImportance.objects.get(training_model_id=model_id, project_id=project_id)
            data = FeatureImportanceSerializer(model, many=False).data
            return Response(data={'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': 'Does not exist', 'success': False}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='loss-interaction')
    def get_lossinteraction(self, request, *args, **kwargs):
        try:
            model_id = kwargs.get('pk', None)
            project_id = request.GET.get('project', None)
            model = LossVsInteraction.objects.get(training_model_id=model_id, project_id=project_id)
            data = LossVsInteractionSerializer(model, many=False).data
            return Response(data={'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': 'Does not exist', 'success': False}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='actual-prediction')
    def get_actualprediction(self, request, *args, **kwargs):
        try:
            model_id = kwargs.get('pk', None)
            project_id = request.GET.get('project', None)
            model = ActualVsPrediction.objects.get(training_model_id=model_id, project_id=project_id)
            data = ActualVsPredictionSerializer(model, many=False).data
            return Response(data={'data': data, 'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': 'Does not exist', 'success': False}, status=status.HTTP_200_OK)


class MetaTypeView(ListAPIView):
    model = MetaType
    serializer_class = MetaTypeSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(MetaTypeView, self).list(request, *args, **kwargs)
        return Response({'success': True, 'results': response.data})


class MetaRoleView(ListAPIView):
    model = MetaRole
    serializer_class = MetaRoleSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(MetaRoleView, self).list(request, *args, **kwargs)
        return Response({'success': True, 'results': response.data})


class MetaImputationView(ListAPIView):
    model = MetaImputation
    serializer_class = MetaImputationSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(MetaImputationView, self).list(request, *args, **kwargs)
        return Response({'success': True, 'results': response.data})

class ProblemTypeView(ListAPIView):
    model = ProblemType
    serializer_class = ProblemTypeSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(ProblemTypeView, self).list(request, *args, **kwargs)
        return Response({'success': True, 'results': response.data})

class TimeTypeView(ListAPIView):
    model = TimeType
    serializer_class = TimeTypeSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(TimeTypeView, self).list(request, *args, **kwargs)
        return Response({'success': True, 'results': response.data})

class TrainingMetricView(ListAPIView):
    model = Metric
    serializer_class = MetricSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(TrainingMetricView, self).list(request, *args, **kwargs)
        return Response({'success': True, 'results': response.data})
