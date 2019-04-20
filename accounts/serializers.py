from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'