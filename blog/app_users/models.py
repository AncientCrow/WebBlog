from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
        Моедль профиля пользователя, является дополнением к модели User,
        и предоставляет дополнительные данные о пользователе.

        Attributes:
        ___________
        * icon - изображение профиля
        * user - соединение с моделью User
        * about - информация о пользователе, которую он может написать
        * birthday - день рождения пользователя
        * followers - поле с отношением многие ко многим, содержит в себе id подписчиков
    """
    icon = models.ImageField(default='default/no_image.png', upload_to='users', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    about = models.TextField(max_length=10000, null=True, verbose_name='about')
    birthday = models.DateField(verbose_name='birthday')
    followers = models.ManyToManyField(User, related_name='following',
                                       blank=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        ordering = ('id',)

    def get_absolute_url(self):
        return f'/users/{self.user.username}/'

    def __str__(self):
        return str(self.user.username)
