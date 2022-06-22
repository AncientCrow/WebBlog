from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserList.as_view(), name='users'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path("registration/", views.RegistrationPage.as_view(), name="registration"),
    path("login/", views.LoginPage.as_view(), name="login"),
    path("logout/", views.LogoutPage.as_view(), name="logout")
]
