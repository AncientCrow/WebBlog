from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('filter/<int:pk>/', views.UsersFilter.as_view(), name='users_filter'),
    path('user/<username>/', views.UserDetail.as_view(), name='user_detail'),
    path('user/<username>/feed', views.FeedFromFollow.as_view(), name='personal_feed'),
    path('follow/', views.user_follow, name='user_follow'),
    path("registration/", views.RegistrationPage.as_view(), name="registration"),
    path("login/", views.LoginPage.as_view(), name="login"),
    path("logout/", views.LogoutPage.as_view(), name="logout")
]
