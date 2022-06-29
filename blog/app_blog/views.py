from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

from . import serializers
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from . import models


class PostList(ListView):
    queryset = models.Post.published_manager.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/list.html'


class PostDetail(View):

    def get(self, request, year, month, day, post):
        user = request.user
        our_post = get_object_or_404(models.Post, slug=post, status='published',
                                     published__year=year, published__month=month, published__day=day)
        our_post.read_status.add(user.id)
        return render(request, 'blog/post/detail.html', {
            'user': user,
            'post': our_post,
            'section': 'posts',
            'status': True, }
                      )


class PostFilter(View):

    def get(self, request, action):
        if action == 1:
            posts = models.Post.published_manager.order_by('-published')
        elif action == 2:
            posts = models.Post.published_manager.order_by('published')
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'blog/post/list.html', {
            'posts': posts,
            'page': page,
            'section': 'posts'
        })


class PostReadFilter(View):

    def get(self, request, status):
        user = request.user
        if status == "read":
            posts = models.Post.objects.filter(read_status__in=[user.id])
        else:
            posts = models.Post.objects.exclude(read_status__in=[user.id])
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'blog/post/list.html', {
            'posts': posts,
            'page': page,
            'section': 'posts'
        })


class PostListAPI(ListAPIView):
    """
        A view for displaying an endpoint with a list of posts.

        Arguments
        _________
        * queryset - responsible for collecting objects inside the database for subsequent display and transmission
        in JSON format;
        * serializer_class - responsible for converting model data into API-friendly format (JSON) and conversely;
        * filter_backends - responsible for filters available on the endpoint
        * ordering_fields - responsible for fields that are affected by the filter
    """
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['published', 'id']


class PostDetailAPI(RetrieveUpdateAPIView):
    """
        A view for displaying an endpoint with detail information information of post, where users can read & delete information.

        Arguments
        _________
        * queryset - responsible for collecting objects inside the database for subsequent display and transmission
        in JSON format;
        * serializer_class - responsible for converting model data into API-friendly format (JSON) and conversely;

    """
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def put(self, request, *args, **kwargs):
        """
            The function allows you to create new information in the database or completely replace the existing one

            Fields
            ______
            * "author": int - user id in database
            * "title": str - name of your post
            * "slug": str - slug name of your post (usually equal to the title)
            * "text": str - text into post,
            * "published": str - date and time when post was added
            * "status": str - one of the available statuses (published, draft, moderation)
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
            The function allow you to update old information in the database but this information may be partial

            Fields
            ______
            * "author": int - user id in database
            * "title": str - name of your post
            * "slug": str - slug name of your post (usually equal to the title)
            * "text": str - text into post,
            * "published": str - date and time when post was added
            * "status": str - one of the available statuses (published, draft, moderation)
        """
        return self.partial_update(request, *args, **kwargs)


class SwaggerDocumentation(APIView):
    """
        Open the documentation page
    """
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer,
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)