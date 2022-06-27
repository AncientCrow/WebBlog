from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from app_users.models import Profile


class UserListTest(TestCase):

    def test_url_exist(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name(self):
        response = self.client.get(reverse('users:user_list'))
        self.assertEqual(response.status_code, 200)

    def test_url_use_valid_template(self):
        response = self.client.get(reverse('users:user_list'))
        self.assertTemplateUsed(response, "users/user/list.html")


class RegistrationTest(TestCase):

    def test_url_exist(self):
        response = self.client.get('/users/registration/')
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name(self):
        response = self.client.get(reverse('users:registration'))
        self.assertEqual(response.status_code, 200)

    def test_url_use_valid_template(self):
        response = self.client.get(reverse('users:registration'))
        self.assertTemplateUsed(response, 'users/user/registration.html')


class UsersFilterTest(TestCase):
    # добавить исключение при неверном фильтре
    def test_url_exist_filter_more(self):
        response = self.client.get('/users/filter/{}/'.format(1))
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name_filter_more(self):
        response = self.client.get(reverse('users:users_filter', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_url_exist_filter_less(self):
        response = self.client.get('/users/filter/{}/'.format(2))
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name_filter_less(self):
        response = self.client.get(reverse('users:users_filter', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)

    def test_url_use_valid_template_more(self):
        response = self.client.get(reverse('users:users_filter', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, "users/user/list.html")

    def test_url_use_valid_template_less(self):
        response = self.client.get(reverse('users:users_filter', kwargs={'pk': 2}))
        self.assertTemplateUsed(response, "users/user/list.html")


class UserDetailTest(TestCase):

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

    def test_url_exist(self):
        response = self.client.get('/users/user/{}/'.format(self.profile.user.username))
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name(self):
        response = self.client.get(reverse('users:user_detail', kwargs={'username': self.profile.user.username}))
        self.assertEqual(response.status_code, 200)

    def test_url_use_valid_template(self):
        response = self.client.get(reverse('users:user_detail', kwargs={'username': self.profile.user.username}))
        self.assertTemplateUsed(response, 'users/user/detail.html')


class LoginPageTest(TestCase):

    def test_url_exist(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_url_use_valid_template(self):
        response = self.client.get(reverse('users:login'))
        self.assertTemplateUsed(response, 'users/user/login.html')


class LogoutTest(TestCase):
    # logout перенаправляет на список пользователей
    def test_url_exist(self):
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)

    def test_url_exist_by_name(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)


class FollowTest(TestCase):

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

    def test_url_exist_get(self):
        self.client.login(username='test', password='123qwe!@#')
        response = self.client.get('/users/follow/')
        self.assertRedirects(response, '/users/')

    def test_url_exist_post(self):
        self.client.login(username='test', password='123qwe!@#')
        profile = self.profile.user.username
        response = self.client.post('/users/follow/')
        self.assertRedirects(response, '/users/user/{}/'.format(profile))