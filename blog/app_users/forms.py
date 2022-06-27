import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
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

    class Meta:
        model = User
        fields = ['username', 'date']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
