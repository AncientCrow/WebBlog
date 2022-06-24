from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    follow_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-follow_date',)

    def __str__(self):
        return '{} follows {}'.format(self.follower, self.followed)


class Profile(models.Model):
    icon = models.ImageField(default='default/no_image.png', upload_to='users', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    about = models.TextField(max_length=10000, null=True, verbose_name='about')
    birthday = models.DateField(verbose_name='birthday')

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def get_absolute_url(self):
        return f'/user/{self.id}'


# модель пользователя не определена, требуется динамическое добавление
User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Follow,
                                         related_name='followers',
                                         symmetrical=False)
                  )
