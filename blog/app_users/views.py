from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django_filters import ChoiceFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter

from . import forms, models
from app_blog import models as post_models
from app_users import serializers

from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView


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
        user = get_object_or_404(models.User, username=username)
        profile = get_object_or_404(models.Profile, user=user)
        return render(request, 'users/user/detail.html', {
            'profile': profile,
            'section': 'profile'}
                      )


class LoginPage(LoginView):
    template_name = 'users/user/login.html'
    authentication_form = forms.LoginForm


class LogoutPage(LogoutView):
    pass


def user_follow(request):
    if request.method == 'POST':
        follower = models.Profile.objects.get(user=request.user)
        profile_id = request.POST.get('profile_id')
        followed = models.Profile.objects.get(pk=profile_id)
        if follower.user in followed.followers.all():
            followed.followers.remove(follower.user)
        else:
            followed.followers.add(follower.user)
        return redirect('users:user_detail', followed.user.username)
    return redirect('users:user_list')


class FeedFromFollow(View):

    def get(self, request, username):
        username = models.User.objects.get(username=username)
        profiles = models.Profile.objects.filter(followers__in=[username.id])
        profiles = [user.user.id for user in profiles]
        posts = post_models.Post.objects.filter(author__in=profiles, status='published').order_by('-published')
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.get_page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'users/user/feeds.html', {
            'posts': posts,
            'page': posts,
            'section': 'posts'
        })


class UserListAPI(ListAPIView):
    """
        A view for displaying an endpoint with a list of users.

        Arguments
        _________
        * queryset - responsible for collecting objects inside the database for subsequent display and transmission
        in JSON format;
        * serializer_class - responsible for converting model data into API-friendly format (JSON) and conversely;
        * filter_backends - responsible for filters available on the endpoint
        * ordering_fields - responsible for fields that are affected by the filter
    """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['date_joined', ]


class UserDetailAPI(RetrieveAPIView):
    """
        A view for displaying an endpoint with detail information about user.

        Arguments
        _________
        * queryset - responsible for collecting objects inside the database for subsequent display and transmission
        in JSON format;
        * serializer_class - responsible for converting model data into API-friendly format (JSON) and conversely;

    """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        """
            The function allows you to create new information in the database or completely replace the existing one

            Fields
            ______
            * "id": int - user's index in database,
            * "is_staff": boolean - true or false (moderator or not),
            * "username": str - just user's nickname,
            * "first_name": str,
            * "last_name": str,
            * "email": str
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
            The function allow you to update old information in the database but this information may be partial

            Fields
            ______
            * "id": int - user's index in database,
            * "is_staff": boolean - true or false (moderator or not),
            * "username": str - just user's nickname,
            * "first_name": str,
            * "last_name": str,
            * "email": str
        """
        return self.partial_update(request, *args, **kwargs)


class ProfileListAPI(ListAPIView):
    """
        A view for displaying an endpoint with a list of user's profile.

        Arguments
        _________
        * queryset - responsible for collecting objects inside the database for subsequent display and transmission
        in JSON format;
        * serializer_class - responsible for converting model data into API-friendly format (JSON) and conversely;
        * filter_backends - responsible for filters available on the endpoint
        * ordering_fields - responsible for fields that are affected by the filter
    """

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['user__date_joined', ]


class ProfileDetailAPI(RetrieveUpdateAPIView):
    """
        A view for displaying an endpoint with detail information about user's profile.

        Arguments
        _________
        * queryset - responsible for collecting objects inside the database for subsequent display and transmission
        in JSON format;
        * serializer_class - responsible for converting model data into API-friendly format (JSON) and conversely;

    """
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        """
            The function allows you to create new information in the database or completely replace the existing one

            Fields
            ______
            * "user": int - user id in database,
            * "about": str - text about user,
            * "birthday": str - user's date of birth,
            * "followers": str - list of user ids in format [ 1,2,3,etc ]
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
            The function allow you to update old information in the database but this information may be partial

            Fields
            ______
            * "user": int - user id in database,
            * "about": str - text about user,
            * "birthday": str - user's date of birth,
            * "followers": str - list of user ids in format [ 1,2,3,etc ]
        """
        return self.partial_update(request, *args, **kwargs)
