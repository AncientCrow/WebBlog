from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('filter/<int:pk>/', views.UsersFilter.as_view(), name='users_filter'),
    path('user/<username>/', views.UserDetail.as_view(), name='user_detail'),
    path('user/<username>/feed/', views.FeedFromFollow.as_view(), name='personal_feed'),
    path('follow/', views.user_follow, name='user_follow'),
    path("registration/", views.RegistrationPage.as_view(), name="registration"),
    path("login/", views.LoginPage.as_view(), name="login"),
    path("logout/", views.LogoutPage.as_view(), name="logout"),
    path('user_api/', views.UserListAPI.as_view(), name='user_list_api'),
    path('user_api/<int:id>/', views.UserDetailAPI.as_view(), name='user_detail_api'),
    path('profile_api/', views.ProfileListAPI.as_view(), name='profile_list_api'),
    path('profile_api/<int:id>/', views.ProfileDetailAPI.as_view(), name='profile_detail_api')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
