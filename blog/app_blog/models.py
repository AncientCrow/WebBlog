from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from transliterate import slugify, translit


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    """
        Модель профиля пользователя, является дополнением к модели User,
        и предоставляет дополнительные данные о пользователе.

        Attributes:
        ___________
        * title - название поста
        * slug - слаг, для создания url-а
        * author - создатель поста
        * text - текст поста
        * published - дата публикации поста
        * created - дата создания поста
        * updated - дата обновления поста
        * status - статус поста из 3-х доступных (черновик/модерируется/опубликовано)
        * read_status - поле с отношением многие ко многим, сохраняющее информации о пользователях, прочитавиш пост
    """

    STATUS = (
        ('draft', 'Черновик'),
        ('moderation', 'Модерируется'),
        ('published', 'Опубликовано'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    text = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS, default='draft')
    objects = models.Manager()
    published_manager = PublishedManager()
    read_status = models.ManyToManyField(User, related_name='checked', blank=True)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.published.year, self.published.month, self.published.day, self.slug])

    def save(self, *args, **kwargs):
        title = translit(self.title, 'ru')
        self.slug = slugify(title)
        super(Post, self).save(*args, **kwargs)
