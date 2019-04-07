from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class MetaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaType
        fields = '__all__'


class MetaRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaRole
        fields = '__all__'


class MetaImputationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaImputation
        fields = '__all__'


class MetaSerializer(serializers.ModelSerializer):
    type_d = MetaTypeSerializer(many=False, read_only=True, source='type')
    role_d = MetaRoleSerializer(many=False, read_only=True, source='role')
    imputation_d = MetaImputationSerializer(many=False, read_only=True, source='imputation')
    class Meta:
        model = Meta
        fields = '__all__'


class DatasetMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = '__all__'

class TestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingData
        fields = '__all__'

class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graph
        fields = '__all__'

class DatasetSerializer(serializers.ModelSerializer):
    metas = MetaSerializer(many=True, read_only=True)
    class Meta:
        model = DataSet
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    datasets = DatasetMinimalSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        obj = super(ProjectSerializer, self).create(validated_data)
        user = self.context['request'].user
        obj.user = user
        obj.save()
        return obj

class ProjectMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class MetaMinimalSerializer(serializers.ModelSerializer):
    dataset = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Meta
        fields = ('id', 'column_name', 'dataset')

    def get_dataset(self, obj):
        return {'id': obj.data.id, 'name': obj.data.name}


class MergeColumnSerializer(serializers.ModelSerializer):
    from_column_d = MetaMinimalSerializer(many=False, read_only=True, source='from_column')
    to_column_d = MetaMinimalSerializer(many=False, read_only=True, source='to_column')
    class Meta:
        model = MergeColumn
        fields = ('id', 'from_column', 'to_column', 'project', 'from_column_d', 'to_column_d')


class ProblemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemType
        fields = '__all__'

class TimeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeType
        fields = '__all__'

class ForecastGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastGroupBy
        fields = '__all__'


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'


class TrainingModelSerializer(serializers.ModelSerializer):
    # metric = MetricSerializer(many=False, read_only=True)
    class Meta:
        model = TrainingModel
        fields = ('name', 'id', 'training',)


class TrainingDetailSerializer(serializers.ModelSerializer):
    y_yariable_d = MetaSerializer(many=False, read_only=True, source='y_yariable')
    time_yariable_d = MetaSerializer(many=False, read_only=True, source='time_yariable')
    problem_type_d = ProblemTypeSerializer(many=False, read_only=True, source='problem_type')
    # forecast_group_by = ForecastGroupSerializer(many=False, read_only=True)
    processed_file_d = DatasetSerializer(many=False, read_only=True, source='processed_file')
    class Meta:
        model = TrainingDetail
        fields = '__all__'

    def create(self, validated_data):
        obj = super(TrainingDetailSerializer, self).create(validated_data)
        obj.project.status = Project.Running
        obj.project.save()
        return obj

class TrainingModelDetailSerializer(serializers.ModelSerializer):
    training = TrainingDetailSerializer(many=False, read_only=True)
    class Meta:
        model = TrainingModel
        fields = ('name', 'id', 'training',)

class DeployedModelSerializer(serializers.ModelSerializer):
    model_d = TrainingModelDetailSerializer(many=False, read_only=True, source='model')
    class Meta:
        model = DeployedModel
        fields = '__all__'

    def create(self, validated_data):
        obj = super(DeployedModelSerializer, self).create(validated_data)
        obj.project.status = Project.Deployed
        obj.project.save()
        return obj


class AccuracySerializer(serializers.ModelSerializer):
    metric = MetricSerializer(many=False, read_only=True)
    class Meta:
        model = ModelMetric
        fields = ('metric','value')


class ROCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ROC
        fields = ('data',)

class BluePrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = BluePrint
        fields = ('data',)

class FeatureImportanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureImportance
        fields = ('data',)

class LossVsInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LossVsInteraction
        fields = ('data',)

class ActualVsPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActualVsPrediction
        fields = ('data',)

class GraphTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphType
        fields = ('name',)

class GraphSerializer(serializers.ModelSerializer):
    type = GraphTypeSerializer(many=False, read_only=True)
    class Meta:
        model = Graph
        fields = ('name','type','data', 'csv_url')
