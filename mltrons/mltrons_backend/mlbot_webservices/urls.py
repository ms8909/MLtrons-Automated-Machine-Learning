"""mlbot_webservices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from mlbot import views
from django.conf.urls.static import static


# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='Mlbot API')

#from drf_yasg.views import get_schema_view
#from drf_yasg import openapi
from rest_framework import permissions


admin.site.site_header = settings.ADMIN_SITE_HEADER

#schema_view = get_schema_view(
#   openapi.Info(
#      title="Snippets API",
#      default_version='v1',
#   ),
#   public=True,
#   permission_classes=(permissions.AllowAny,),
#)

urlpatterns = [
    # url(r'^$', schema_view),
 #   url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  #  url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
   #                   name='schema-json'),
    url(r'^admin/', admin.site.urls),
    # url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^jet/', include('jet.urls', 'jet')),
    # url(r'^mlbot/', include('mlbot.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^apis/', include('project.urls')),
    # url(r'^csvParser/', views.csvParserView.as_view()),
    # url(r'^newGraph/', views.newGraphReqest.as_view()),
    # url(r'^createGraph/', views.createGraph.as_view()),
    # url(r'^allGraphs/', views.generateAllGraphs.as_view()),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^createGraph/', views.createGraph.as_view()),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
