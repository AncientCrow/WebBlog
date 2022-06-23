from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from . import models


class PostsFeed(Feed):
    title = 'Наш блог'
    link = '/blog/'
    description = 'новые новости блога'

    def items(self):
        # пока на 5 последних постов
        return models.Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.text, 20)