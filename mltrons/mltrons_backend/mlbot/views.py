# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework.decorators import list_route, detail_route
from django.urls import reverse
from rest_framework.response import Response
from mlbot.serializers import  UserDocsSerializer, UserDashboardSerializer
from rest_framework import status
import requests
from django.conf import settings
from mlbot.models import UserDocs, UserDashboard, DashboardGraphs
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os.path
import pickle
import io
import datetime
import gc
import dill
from django.contrib.auth import get_user_model
User = get_user_model()
import json

## that's where you need to decide where and how to store the data
## and tbh mongo db here is not a bad option or go for sql
class csvParserView(APIView):
    permission_classes = ()
    def post(self, request):
        try:
            if request.FILES and request.FILES['file_url']:
                myfile = request.FILES['file_url']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.path(filename)
                df=pd.read_csv(uploaded_file_url, nrows=6)

                dict= df.to_dict()

                for k in dict.keys():
                    for key in dict[k].keys():
                        if type(key) is not str:
                            try:
                                dict[k][str(key)] = dict[k][key]
                                dict[k][str(key)] = str(dict[k][str(key)])
                            except:
                                try:
                                    dict[k][repr(key)] = dict[k][key]
                                    dict[k][repr(key)] = str(dict[k][repr(key)])
                                except:
                                    pass
                            del dict[k][key]
                return Response({'data': json.dumps(dict)}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'something went wrong. please check log for details.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'something went wrong. please check log for details.'},
                            status=status.HTTP_400_BAD_REQUEST)



class newGraphReqest(APIView):
    permission_classes = ()
    def post(self, request):

        dashboard_id = request.data.get('dashboard_id', None)


        try:
            if dashboard_id:
                dashboard=UserDashboard.objects.get(id=dashboard_id)
                csv_file = dashboard.dashboard_url

                # file = open(csv_file.path, 'r')
                # gc.disable()
                # file_object=pickle.load(file)
                # gc.enable()
                # key = file_object.prediction_key()
                key=dashboard.graph_key;
                # key = [-1, list(key[0]), key[1]]
                # file.close()
                # with open(csv_file.path, 'wb') as f:
                #     pickle.dump(file_object, f)
                #     f.close()
                #key=[0,['var1','var2','var3'],{'datemonth':{}, 'dateyear':{}, 'dateday':{:{'opt1': '1', 'opt2':'2'}, 'var1':{}}}, 'var']

                return Response({'data': key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'something went wrong. please check log for details.'}, status=status.HTTP_400_BAD_REQUEST)
        except UserDashboard.DoesNotExist as e:
            return Response({'error': 'Failed! invalid dashboard.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'something went wrong. please check log for details.'},
                            status=status.HTTP_400_BAD_REQUEST)



## 
class createGraph(APIView):
    permission_classes = ()
    def post(self, request):

        dashboard_id = request.data.get('dashboard_id', None)
        data = request.data.get('data', None)
        index = request.data.get('index', None)

        data1=json.loads(data)

        try:
            if dashboard_id:
                dashboard=UserDashboard.objects.get(id=dashboard_id)
                file1 = open(dashboard.dashboard_url.path, 'r+')
                gc.disable()
                file_object=pickle.load(file1)
                gc.enable()

                index2= file_object.make_graph_object()
                graph_dataframe= file_object.make_graph(index2,data1)

                basename = "graph"
                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                file_name = "_".join([basename, suffix]) + ".pickle"  # e.g. 'mylogfile_120508_171442'

                path = os.path.join(settings.MEDIA_ROOT, 'Images', 'User', 'Graphs', file_name);
                print(path)

                file = open(path, 'w+')
                pickle.dump(graph_dataframe, file)
                file.close()

                graph = DashboardGraphs.objects.create(dashboard=dashboard, graph_url='Images/User/Graphs/'+file_name, graph_input_data= data)
                graph.save()
                return Response({'data': 'graph created successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'something went wrong. please check log for details.'}, status=status.HTTP_400_BAD_REQUEST)
        except UserDashboard.DoesNotExist as e:
            return Response({'error': 'Failed! invalid dashboard.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'something went wrong. please check log for details.'},
                            status=status.HTTP_400_BAD_REQUEST)





class generateAllGraphs(APIView):
    permission_classes = ()
    def post(self, request):

        dashboard_id = request.data.get('dashboard_id', None)


        try:
            if dashboard_id:
                dashboard=UserDashboard.objects.get(id=dashboard_id)
                graphs= DashboardGraphs.objects.filter(dashboard=dashboard)

                all_graphs=[]

                for graph in graphs:
                    file=open(graph.graph_url.path, 'r+')
                    graph_object=pickle.load(file)
                    dict = graph_object[1].to_dict()

                    for k in dict.keys():
                        for key in dict[k].keys():
                            if type(key) is not str:
                                try:
                                    dict[k][str(key)] = dict[k][key]
                                    dict[k][str(key)] = str(dict[k][str(key)])
                                except:
                                    try:
                                        dict[k][repr(key)] = dict[k][key]
                                        dict[k][repr(key)] = str(dict[k][repr(key)])
                                    except:
                                        pass
                                del dict[k][key]

                    all_graphs.append([dict,graph.graph_input_data])
                    file.close()


                return Response({'data': json.dumps(all_graphs)}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'something went wrong. please check log for details.'}, status=status.HTTP_400_BAD_REQUEST)
        except UserDashboard.DoesNotExist as e:
            return Response({'error': 'Failed! invalid dashboard.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'something went wrong. please check log for details.'},
                            status=status.HTTP_400_BAD_REQUEST)


class UserDashboardViewSet(viewsets.ModelViewSet):
    # permission_classes = [TokenHasScope]
    # required_scopes = ['read', 'write', 'guest']
    queryset = UserDashboard.objects.all()
    serializer_class = UserDashboardSerializer

    # lookup_field = 'id'

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        """
        List all User Docs

        ---
        parameters:
            - name: limit
              type: string
              required: false
              paramType: query
            - name: offset
              type: string
              required: false
              paramType: query

        """
        return super(UserDashboardViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create new User Document

        """
        user_id = request.data.get('user', None)
        # user_id = request.user.id
        # log_dict = helper_functions.get_log_dict(request)
        response = super(UserDashboardViewSet, self).create(request, *args, **kwargs)
        return response


    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a particular User Doc

        """
        return super(UserDashboardViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a particular User Doc

        """
        return super(UserDashboardViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial Update a particular User Doc

        """
        # log_dict = helper_functions.get_log_dict(request)
        response = super(UserDocsViewSet, self).partial_update(request, *args, **kwargs)
        return response

    def destroy(self, request, *args, **kwargs):
        """
        Delete a particular UserDocs

        """
        return super(UserDashboardViewSet, self).destroy(request, *args, **kwargs)








class UserDocsViewSet(viewsets.ModelViewSet):
    # permission_classes = [TokenHasScope]
    # required_scopes = ['read', 'write', 'guest']
    queryset = UserDocs.objects.all()
    queryset = UserDocsSerializer.setup_eager_loading(queryset)
    serializer_class = UserDocsSerializer

    # lookup_field = 'id'

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        """
        List all User Docs

        ---
        parameters:
            - name: limit
              type: string
              required: false
              paramType: query
            - name: offset
              type: string
              required: false
              paramType: query

        """
        return super(UserDocsViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create new User Document

        """
        user_id = request.data.get('user', None)
        # user_id = request.user.id
        # log_dict = helper_functions.get_log_dict(request)
        response = super(UserDocsViewSet, self).create(request, *args, **kwargs)
        return response


    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a particular User Doc

        """
        return super(UserDocsViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a particular User Doc

        """
        return super(UserDocsViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial Update a particular User Doc

        """
        # log_dict = helper_functions.get_log_dict(request)
        response = super(UserDocsViewSet, self).partial_update(request, *args, **kwargs)
        return response

    def destroy(self, request, *args, **kwargs):
        """
        Delete a particular UserDocs

        """
        return super(UserDocsViewSet, self).destroy(request, *args, **kwargs)
