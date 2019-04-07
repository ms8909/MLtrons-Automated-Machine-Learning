from rest_framework import serializers
from mlbot.models import UserDocs, UserDashboard
from oauth2_provider.models import AccessToken
from project.serializers import ProjectMinimalSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserDashboardSerializer(serializers.ModelSerializer):
    docs_dashboard = serializers.SerializerMethodField('get_latest_docs')

    def get_latest_docs(self, obj):
        request = self.context.get('request')

        try:
            latest_docs = obj.docs_dashboard.filter(doc_status='Pending').latest('id')
            return UserDocsSerializer(latest_docs, many=False).data
        except UserDocs.DoesNotExist:
            return None


    class Meta:
        model = UserDashboard
        fields = "__all__"


class UserDocsSerializer(serializers.ModelSerializer):
    # file_url = serializers.SerializerMethodField()
    #
    # def get_file_url(self, obj):
    #     # request = self.context.request
    #     request = self.context.get('request')
    #     if obj.file_url is not None:
    #         # return request.META['wsgi.url_scheme'] + '://' + request.META['HTTP_HOST'] + obj.image.url
    #         return request.build_absolute_uri(obj.file_url.url)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """

        return queryset

    class Meta:
        model = UserDocs
        fields = '__all__'
