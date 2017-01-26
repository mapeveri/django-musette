from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .models import Category, Forum, Topic


class TopicFeed(Feed):
    # attr basic of feed
    title = 'Forum rss'
    description = 'Feed for forums'

    def get_object(self, request, *args, **kwargs):
        category = get_object_or_404(Category, name=kwargs['category'])
        forum = get_object_or_404(
            Forum, category__name=category, name=kwargs['forum']
        )
        return forum

    def items(self, forum):
        # Get forum
        return Topic.objects.filter(forum_id=forum.idforum)

    def item_link(self, item):
        return reverse("topic", args=[
            item.forum.category.name, item.forum.name, item.slug, item.idtopic
        ])

    def link(self, forum):
        return reverse('rss', args=[
            forum.category.name, forum.name
        ])

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.date
