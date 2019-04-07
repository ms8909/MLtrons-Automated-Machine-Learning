from django.conf.urls import url,include
from rest_framework import routers
from accounts import views as account_views

router = routers.SimpleRouter()
router.register(r'auth', account_views.AuthOperationsViewSet)

urlpatterns = [
url(r'^', include(router.urls)),
]