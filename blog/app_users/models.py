from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    icon = models.ImageField(default='default/no_image.png', upload_to='users', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    about = models.TextField(max_length=10000, null=True, verbose_name='about')
    birthday = models.DateField(verbose_name='birthday')
    followers = models.ManyToManyField(User, related_name='following',
                                       blank=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def get_absolute_url(self):
        return f'/user/{self.id}'

    def __str__(self):
        return str(self.user.username)
