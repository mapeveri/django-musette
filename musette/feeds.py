from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .models import Forum, Topic


class TopicFeed(Feed):
    # attr basic of feed
    title = 'Forum rss'
    description = 'Feed for forums'

    def get_object(self, request, *args, **kwargs):
        return kwargs['forum']

    def items(self, forum):
        forum = get_object_or_404(Forum, name=forum)
        return Topic.objects.filter(forum_id=forum.idforum)

    def item_link(self, item):
        return reverse("topic", args=[
            item.forum.name, item.slug, item.idtopic]
        )

    def link(self, item):
        return "/feed/" + item + "/"

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.date
