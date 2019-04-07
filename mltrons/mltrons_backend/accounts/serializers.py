from rest_framework import serializers
from oauth2_provider.models import AccessToken
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    @staticmethod
    def get_token(obj):
        try:
            token = AccessToken.objects.filter(user=obj).values('token', 'expires')
            if token:
                return token.latest('id')
            else:
                return None
        except Exception as e:
            print(e)
            return None
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'company_name',
                  'token')

class RegisterSerializer(serializers.ModelSerializer):
    confirm = serializers.CharField()
    def validate(self, data):
        try:
            user = User.objects.filter(email=data.get('email'))
            if len(user) > 0:
                raise serializers.ValidationError("Email already exists")
        except User.DoesNotExist:
            pass

        if not data.get('password') or not data.get('confirm'):
            raise serializers.ValidationError("Empty Password")

        if data.get('password') != data.get('confirm'):
            raise serializers.ValidationError("Password Mismatch")
        return data

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'company_name', 'email', 'password', 'confirm')
        extra_kwargs = {'confirm': {'read_only': True}}

    def create(self, validated_data):
        del validated_data['confirm']
        user = super(RegisterSerializer, self).create(validated_data)
        user.username=validated_data['email']
        user.set_password(validated_data['password'])
        user.save()
        return user