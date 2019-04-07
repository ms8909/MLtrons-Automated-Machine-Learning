from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework.decorators import list_route, detail_route
from django.urls import reverse
from rest_framework.response import Response
from accounts.serializers import UserSerializer, RegisterSerializer
from rest_framework import status
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
import json
User = get_user_model()


class AuthOperationsViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(methods=['post'])
    def login(self, request, *args, **kwargs):
        """
        API to login a user

        """
        params = dict()
        params['username'] = request.data['email']
        params['password'] = request.data['password']
        params['client_id'] = settings.APP_CLIENT_ID
        params['client_secret'] = settings.APP_CLIENT_SECRET
        params['grant_type'] = 'password'
        params['scope'] = 'read write guest admin'
        # log_dict = helper_functions.get_log_dict(request)

        try:
            user = User.objects.get(email=params['username'], is_active=True)
        except User.DoesNotExist:
            msg = "User does not exist against the provided email address."
            return Response({"error": msg, "success": False}, status=status.HTTP_417_EXPECTATION_FAILED)
        try:
            url = request.build_absolute_uri(reverse('oauth2_provider:token', *args, **kwargs))
            # headers = {'Authorization': 'Bearer ' + request.auth.token}
            response = requests.post(url, data=params)  # , headers=headers
            if response.status_code != status.HTTP_200_OK:
                return Response(data=response.json(), status=response.status_code)

            serializer = UserSerializer(user, many=False)
            data = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"detail": "Failed! Something went wrong. Please watch logs for detail"},
                            status=status.HTTP_417_EXPECTATION_FAILED)


    @list_route(methods=['post'])
    def register(self, request, *args, **kwargs):
        if request.auth is None:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()
                        return Response(data={}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(data={"error": e}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)