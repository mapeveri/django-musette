from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import (
	ForumsView, ForumView, TopicView, NewTopicView,
	EditTopicView, DeleteTopicView, NewCommentView,
	EditCommentView, DeleteCommentView, AllNotification,
	SetNotifications
)

urlpatterns = [
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
		TopicView, name='topic'
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
		r'^forum_all_notification/$', login_required(AllNotification),
		name='forum_all_notification'
	),
	url(
		r'^forum_set_notifications/$', login_required(SetNotifications),
		name='forum_set_notifications'
	),
]
