from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from app_users.models import Profile


class ProfileTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test",
                                        email="test@test.ru",
                                        password="123qwe!@#"
                                        )
        user_1 = User.objects.create_user(username="test1",
                                          email="test1@test.ru",
                                          password="123qwe!@#"
                                          )

        self.profile = Profile.objects.create(
            user=self.user,
            about="test_text",
            birthday=timezone.now(),
        )

        self.profile.followers.add(user_1.id)

    def test_absolute_url(self):
        username = self.user.username
        profile = self.profile
        self.assertEqual(profile.get_absolute_url(), '/users/{}/'.format(username))

    def test_about_max_length(self):
        profile = self.profile
        self.assertEqual(profile._meta.get_field('about').max_length, 10000)

    def test_icon_default(self):
        profile = self.profile
        self.assertEqual(profile._meta.get_field('icon').default, 'default/no_image.png')

