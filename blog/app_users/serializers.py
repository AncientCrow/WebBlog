from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from . import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['id', 'user', 'about', 'birthday', 'followers']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    user_id = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'is_staff', 'username', 'first_name', 'last_name', 'email', 'user_id']