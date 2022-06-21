from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    STATUS = (
        ('draft', 'Черновик'),
        ('moderation', 'Модерируется'),
        ('published', 'Опубликовано'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    text = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS, default='draft')

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
