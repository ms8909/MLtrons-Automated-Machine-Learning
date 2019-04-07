from django.conf.urls import url,include
from rest_framework import routers
from mlbot import views as mlmot_views

router = routers.SimpleRouter()
router.register(r'docs', mlmot_views.UserDocsViewSet)
router.register(r'dashboard', mlmot_views.UserDashboardViewSet)

urlpatterns = [
url(r'^', include(router.urls)),
]