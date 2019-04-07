from django.conf.urls import url,include
from rest_framework import routers
from project import views as project_views

router = routers.SimpleRouter()
router.register(r'project', project_views.ProjectViewSet, base_name='project')
router.register(r'dataset', project_views.DataSetViewSet, base_name='dataset')
router.register(r'meta', project_views.MetaViewSet, base_name='metas')
router.register(r'connection', project_views.MetaConnectionViewSet, base_name='connection')
router.register(r'training', project_views.TrainingDetailViewSet, base_name='training')
router.register(r'testing', project_views.TestingModelViewSet, base_name='testing')
router.register(r'models', project_views.TrainingModelViewSet, base_name='models')
router.register(r'deploy', project_views.DeployedModellViewSet, base_name='deploy')

urlpatterns = [
url(r'meta/type', project_views.MetaTypeView.as_view(), name='meta-role'),
url(r'meta/role', project_views.MetaRoleView.as_view(), name='meta-type'),
url(r'meta/imputation', project_views.MetaImputationView.as_view(), name='meta-imputation'),
url(r'training/problem', project_views.ProblemTypeView.as_view(), name='training-problem'),
url(r'training/time', project_views.TimeTypeView.as_view(), name='training-time'),
url(r'training/metric', project_views.TrainingMetricView.as_view(), name='training-metric'),
url(r'task/progress', project_views.get_task_progress, name='task_progress'),
url(r'^', include(router.urls)),
]