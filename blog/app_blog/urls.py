from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('filter/<int:pk>/', views.PostFilter.as_view(), name='post_filter'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.PostDetail.as_view(), name='post_detail'),
    ]
