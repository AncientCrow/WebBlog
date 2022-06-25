from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

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

