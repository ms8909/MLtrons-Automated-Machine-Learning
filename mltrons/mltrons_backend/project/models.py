from django.db import models
from mlbot.models import User
from mlbot_webservices.shared_utils import UploadToPathAndRename
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class MetaType(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class MetaRole(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class MetaImputation(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class Project(models.Model):
    Pending = 'Pending'
    Running = 'Running'
    Completed = 'Completed'
    Deployed = 'Deployed'
    Failed = 'Failed'

    STATUS_CHOICES = (
        (Pending, 'Pending'),
        (Running, 'Running'),
        (Completed, 'Completed'),
        (Deployed, 'Deployed'),
        (Failed, 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    status = models.CharField(max_length=37, choices=STATUS_CHOICES, default=Pending)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name


class Task(models.Model):
    Pending = 'Pending'
    Running = 'Running'
    Completed = 'Completed'

    STATUS_CHOICES = (
        (Pending, 'Pending'),
        (Running, 'Running'),
        (Completed, 'Completed'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_tasks', null=True, blank=True)
    task_id = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=37, choices=STATUS_CHOICES, default=Pending)
    created_at = models.DateTimeField(default=timezone.now)


class DataSet(models.Model):
    UnProcessed = 'UnProcessed'
    Processed = 'Processed'
    STATUS_CHOICES = (
        (UnProcessed, 'UnProcessed'),
        (Processed, 'Processed'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='datasets')
    name = models.CharField(max_length=256)
    file_url = models.FileField(upload_to=UploadToPathAndRename('User/Datasets'), null=True, blank=True)  # media/
    frame_path = models.CharField(max_length=100, null=True, blank=True)
    rows = models.IntegerField(default=0)
    suffix = models.CharField(max_length=10, null=True, blank=True)
    columns = models.IntegerField(default=0)
    status = models.CharField(max_length=37, choices=STATUS_CHOICES, default=UnProcessed)
    size = models.CharField(max_length=50, null=True, blank=True)
    loc = models.CharField(max_length=50, null=True, blank=True)
    parent = JSONField(null=True, blank=True)
    connections = JSONField(null=True, blank=True)
    grid_map = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()

class UserDataset(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ProjectDataset(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class TestingData(models.Model):
    Pending = 'Pending'
    Completed = 'Completed'
    STATUS_CHOICES = (
        (Pending, 'Pending'),
        (Completed, 'Completed'),
    )
    data = models.ForeignKey(DataSet, on_delete=models.CASCADE, related_name='trainings')
    file_url = models.FileField(upload_to=UploadToPathAndRename('User/Training'), null=True, blank=True)
    frame_path = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=37, choices=STATUS_CHOICES, default=Pending)

class Meta(models.Model):
    data = models.ForeignKey(DataSet, on_delete=models.CASCADE, related_name='metas')
    column_name = models.CharField(max_length=256)
    type = models.ForeignKey(MetaType, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(MetaRole, on_delete=models.CASCADE, null=True, blank=True)
    imputation = models.ForeignKey(MetaImputation, on_delete=models.CASCADE, null=True, blank=True)
    min = models.CharField(max_length=100, default='N/A', null=True, blank=True)
    max = models.CharField(max_length=100, default='N/A', null=True, blank=True)
    missing = models.CharField(max_length=100, default='N/A', null=True, blank=True)
    count = models.CharField(max_length=100, default='N/A', null=True, blank=True)
    mean = models.CharField(max_length=100, default='N/A', null=True, blank=True)
    stdev = models.CharField(max_length=100, default='N/A', null=True, blank=True)
    distribution_data = JSONField(null=True, blank=True)
    def __str__(self):
        return self.column_name

class MergeColumn(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    from_column = models.ForeignKey(Meta, on_delete=models.CASCADE, related_name='from_meta')
    to_column = models.ForeignKey(Meta, on_delete=models.CASCADE, related_name='to_meta')


class ProblemType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class TimeType(models.Model):
    format = models.CharField(max_length=256)
    def __str__(self):
        return self.format


class ForecastGroupBy(models.Model):
    name = models.CharField(max_length=256)
    minutes = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Forecast group by'
        verbose_name_plural = 'Forecasts groups'


class TrainingDetail(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    y_yariable = models.ForeignKey(Meta, on_delete=models.CASCADE, related_name='y_meta')
    time_yariable = models.ForeignKey(Meta, on_delete=models.CASCADE, related_name='time_meta', null=True, blank=True)
    processed_file = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    selected_columns = JSONField(null=True, blank=True)
    problem_type = models.ForeignKey(ProblemType, on_delete=models.CASCADE)
    time_type = models.ForeignKey(TimeType, on_delete=models.CASCADE, null=True, blank=True)
    pipeline_path = models.CharField(max_length=100, null=True, blank=True)
    forecast_group_by = models.ForeignKey(ForecastGroupBy, on_delete=models.CASCADE, null=True, blank=True)
    interupt = models.BooleanField(default=False)

class Metric(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class TrainingModel(models.Model):
    training = models.ForeignKey(TrainingDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=1000)


class DeployedModel(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    model = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)


class ModelMetric(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    model = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)
    value = models.CharField(max_length=100, null=True, blank=True)


class Accuracy(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    training_model = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)
    data = JSONField(null=True, blank=True)


class ROC(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    training_model = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)
    data = JSONField(null=True, blank=True)

class BluePrint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    training_model = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)
    data = JSONField(null=True, blank=True)

class FeatureImportance(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    training_model = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)
    data = JSONField(null=True, blank=True)

class LossVsInteraction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    training_model = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)
    data = JSONField(null=True, blank=True)

class ActualVsPrediction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    training_model = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)
    data = JSONField(null=True, blank=True)

class GraphType(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name

class Graph(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.ForeignKey(GraphType, on_delete=models.CASCADE, null=True, blank=True)
    data = JSONField(null=True, blank=True)
    path = models.CharField(max_length=1000, null=True, blank=True)
    csv_url = models.FileField(upload_to=UploadToPathAndRename('Images/User/Csv'),null=True, blank=True)  # media/

    def __str__(self):
        return self.name
