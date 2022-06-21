from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from . import models


class PostList(ListView):
    queryset = models.Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post,list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post, slug=post, status='published',
                             published__year=year, published__month=month, published__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
