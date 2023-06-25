import io

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = ('slug', 'photo')
