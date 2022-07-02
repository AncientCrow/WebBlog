from django.utils import timezone

from app_users import models as user_models
from app_blog import models as blog_models

from django.contrib.auth.models import User


def create_test_data():
    for index in range(1, 10):
        user = User.objects.create_user(
            username='test{}'.format(index),
            password='123qwe!@#'
        )

        user_models.Profile.objects.create(
            user=user,
            about="test_text",
            birthday=timezone.now(),
        )

        blog_models.Post.objects.create(
            title='test_title{}'.format(index),
            slug='test_title{}'.format(index),
            author=user,
            text='test_text',
            published=timezone.now(),
            created=timezone.now(),
            updated=timezone.now(),
            status='published',
        )

