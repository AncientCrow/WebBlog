from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from . import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['id', 'author', 'title', 'slug', 'text', 'published', 'status']
