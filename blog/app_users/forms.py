import datetime

from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    icon = forms.ImageField(required=False, label='Изображение профиля')
    username = forms.CharField(max_length=25, label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    about = forms.CharField(max_length=10000, required=False)

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


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
