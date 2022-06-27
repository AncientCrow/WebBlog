from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from app_users import forms

from blog.settings import BASE_DIR


class RegistrationFormTest(TestCase):

    def test_form_label(self):
        form = forms.RegistrationForm()
        self.assertTrue(form.fields['icon'].label == 'Изображение профиля')
        self.assertTrue(form.fields['username'].label == 'Логин')
        self.assertTrue(form.fields['password'].label == 'Пароль')
        self.assertTrue(form.fields['password_confirm'].label == 'Повторите пароль')
        self.assertTrue(form.fields['about'].label == 'О себе')
        self.assertTrue(form.fields['birthday'].label == 'День рождения')

    def test_form_values(self):
        image_path = BASE_DIR + '/media/default/no_image.png'
        form_data = {
            'icon': SimpleUploadedFile(
                name='mem.png',
                content=open(image_path, 'rb').read(),
                content_type='image/jpg'
            ),
            'username': 'test',
            'password': '123qwe!@#',
            'password_confirm': '123qwe!@#',
            'birthday': timezone.now(),
            'about': 'test_text'
        }
        form = forms.RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())


class LoginFormTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test",
                                             email="test@test.ru",
                                             password="123qwe!@#"
                                             )

    def test_form_values(self):
        form_data = {
            'username': 'test',
            'password': '123qwe!@#',
        }
        form = forms.LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
