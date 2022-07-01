import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.Form):
    """
        Форма регистрации пользователя

        Attributes
        __________
        * icon - изображение профиля (можно не указывать, будет стандартное изображение)
        * username - имя пользователя
        * password - пароль
        * password_confirm - подтверждение пароля
        * about - информация о пользователя
        * birthday - дата рождения пользователя с максимальным значением в 120 лет( вдруг долгожители)
    """
    icon = forms.ImageField(required=False, label='Изображение профиля')
    username = forms.CharField(max_length=25, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password_confirm = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    about = forms.CharField(max_length=10000, required=False, label='О себе')
    start_year = datetime.date.today().year - 120
    end_year = datetime.date.today().year - 16
    birthday = forms.DateField(
        label='День рождения',
        widget=forms.SelectDateWidget(
            years=range(start_year, end_year)),
    )


class LoginForm(AuthenticationForm):
    """
        Форма входа в профиль пользователя

        Attibutes
        _________

        * username - имя пользователя
        * password - пароль пользователя
    """
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class EditForm(forms.Form):
    """
        Форма редактирования пользователя

        Attributes
        __________

        * about - информация о пользователя
        * birthday - дата рождения пользователя с максимальным значением в 120 лет( вдруг долгожители)
    """
    icon = forms.ImageField(required=False, label='Изображение профиля')
    about = forms.CharField(max_length=10000, required=False, label='О себе')
