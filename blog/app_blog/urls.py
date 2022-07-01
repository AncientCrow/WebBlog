from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('filter/<int:action>/', views.post_filter, name='post_filter'),
    path('filter/<str:status>/', views.PostReadFilter.as_view(), name='post_read_filter'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.PostDetail.as_view(), name='post_detail'),
    path('new_post/', views.NewPost.as_view(), name='new_post'),
    path('post_api/', views.PostListAPI.as_view(), name='post_api_list'),
    path('post_api/<int:id>/', views.PostDetailAPI.as_view(), name='post_detail_api'),
    path('swagger_doc/', views.SwaggerDocumentation.as_view(), name='api_documentation'),
    ]
