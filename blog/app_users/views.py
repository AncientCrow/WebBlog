from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectMixin

from . import forms, models


class RegistrationPage(View):

    def get(self, request):
        registration = forms.RegistrationForm
        return render(request, 'users/user/registration.html', {'form': registration})

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
            return render(request, 'users/user/registration.html', {'form': form})


class UserList(View):

    def get(self, request):
        users_list = models.User.objects.annotate(blog_count=Count('blog_post')).order_by('blog_count')
        paginator = Paginator(users_list, 10)
        page = request.GET.get('page')
        pages = paginator.get_page(page)
        return render(
            request, 'users/user/list.html', {
                'users': pages,
                'section': 'users'}
        )


class UsersFilter(View):

    def get(self, request, pk):
        if pk == 1:
            users_list = models.User.objects.annotate(blog_count=Count('blog_post')).order_by('-blog_count')
        elif pk == 2:
            users_list = models.User.objects.annotate(blog_count=Count('blog_post')).order_by('blog_count')
        paginator = Paginator(users_list, 10)
        page = request.GET.get('page')
        pages = paginator.get_page(page)
        return render(request, 'users/user/list.html', {
            'users': pages,
            'section': 'users'}
                      )


class UserDetail(View):

    def get(self, request, username):
        page_user = get_object_or_404(models.User, username=username)
        return render(request, 'users/user/detail.html', {
            'profile': page_user,
            'section': 'profile'}
                      )


class LoginPage(LoginView):
    template_name = 'users/user/login.html'
    authentication_form = forms.LoginForm


class LogoutPage(LogoutView):
    pass
