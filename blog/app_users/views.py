from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View
from . import forms, models


class RegistrationPage(View):

    def get(self, request):
        registration = forms.RegistrationForm
        return render(request, 'users/registration.html', {'form': registration})

    def post(self, request):
        form = forms.RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            birthday = form.cleaned_data.get('birthday')
            about = form.cleaned_data.get('about')
            icon = form.cleaned_data.get('icon')

            models.Profile.objects.create(
                user=user,
                birthday=birthday,
                about=about,
                icon=icon
            )
            new_user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password")
            )
            login(request, new_user)
            user.save()
            return redirect("post_list")
        else:
            return render(request, 'users/registration.html', {'form': form})


class LoginPage(LoginView):
    template_name = 'user/login.html'
    authentication_form = forms.LoginForm


class LogoutPage(LogoutView):
    pass
