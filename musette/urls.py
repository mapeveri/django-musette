from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from .api import router
from .feeds import TopicFeed
from .views import (
    ForumsView, ForumView, TopicView, NewTopicView,
    EditTopicView, DeleteTopicView, NewCommentView,
    EditCommentView, DeleteCommentView, AllNotification,
    SetNotifications, AddRegisterView, UnregisterView,
    UsersForumView, TopicSearch, ProfileView, EditProfileView
)


admin.site.site_header = settings.SITE_NAME

urlpatterns = [
    #Url for django-rest-framework
    url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    # Url for django-hitcount
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

    # Url's Django-musette
    url(
        r'^forums/$', ForumsView.as_view(), name='forums'
    ),
    url(
        r'^forum/(?P<forum>.+)/$', ForumView.as_view(), name='forum'
    ),
    url(
        r'^topic/(?P<forum>.+)/(?P<slug>[-\w]+)/(?P<idtopic>\d+)/$',
        TopicView.as_view(), name='topic'
    ),
    url(
        r'^newtopic/(?P<forum>.+)/$', login_required(NewTopicView.as_view()),
        name='newtopic'
    ),
    url(
        r'^edit_topic/(?P<forum>.+)/(?P<idtopic>\d+)/$',
        login_required(EditTopicView.as_view()), name='edittopic'
    ),
    url(
        r'^delete_topic/(?P<forum>.+)/(?P<idtopic>\d+)/$',
        login_required(DeleteTopicView.as_view()), name='deletetopic'
    ),
    url(
        r'^newcomment/(?P<forum>.+)/(?P<slug>[-\w]+)/(?P<idtopic>\d+)/$',
        login_required(NewCommentView.as_view()), name='newcomment'
    ),
    url(
        r'^updatecomment/(?P<forum>.+)/(?P<slug>[-\w]+)/(?P<idtopic>\d+)/(?P<idcomment>\d+)/$',
        login_required(EditCommentView.as_view()), name='updatecomment'
    ),
    url(
        r'^removecomment/(?P<forum>.+)/(?P<slug>[-\w]+)/(?P<idtopic>\d+)/(?P<idcomment>\d+)/$',
        login_required(DeleteCommentView.as_view()), name='removecomment'
    ),
    url(
        r'^forum_all_notification/$', login_required(
            AllNotification.as_view()),
        name='forum_all_notification'
    ),
    url(
        r'^forum_set_notifications/$', login_required(SetNotifications),
        name='forum_set_notifications'
    ),
    url(
        r'^new_register/(?P<forum>.+)/$', login_required(
            AddRegisterView.as_view()),
        name='new_register'
    ),
    url(
        r'^unregister/(?P<forum>.+)/$', login_required(UnregisterView.as_view()
                                                       ),
        name='unregister'
    ),
    url(
        r'^users_forum/(?P<forum>.+)/$', UsersForumView.as_view(),
        name='users_forum'
    ),
    url(
        r'^search_topic/(?P<forum>.+)/$', TopicSearch.as_view(),
        name='search_topic'
    ),
    url(
        r'^feed/(?P<forum>.+)/$', TopicFeed(), name='rss'
    ),
    url(
        r'^profile/(?P<username>.+)/$', ProfileView.as_view(), name='profile'
    ),
    url(
        r'^edit_profile/(?P<username>[-\w]+)/$', EditProfileView.as_view(),
        name='edit_profile'
    ),
]