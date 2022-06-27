from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('filter/<int:action>/', views.PostFilter.as_view(), name='post_filter'),
    path('filter/<str:status>/', views.PostReadFilter.as_view(), name='post_read_filter'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.PostDetail.as_view(), name='post_detail'),
    path('post_api/', views.PostListAPI.as_view(), name='ost_api_list'),
    ]
