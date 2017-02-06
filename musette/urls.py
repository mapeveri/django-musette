from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from musette import views
from musette.feeds import TopicFeed
from musette.api.urls import router


admin.site.site_header = settings.SITE_NAME

urlpatterns = [
    # Url for django-rest-framework
    url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    # Url for django-hitcount
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

    # Url's Django-musette
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^join/', views.SignUpView.as_view(), name='signup'),
    url(r'^confirm_email/(?P<username>.+)/(?P<activation_key>\w+)',
        views.ConfirmEmailView.as_view(), name='config_email'),
    url(r'^new_key_activation/(?P<username>.+)',
        views.NewKeyActivationView.as_view(), name='new_key_activation'),
    url(r'^reset_password/$', views.reset_password, name='password_reset'),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset_pass_confirm, name='password_reset_confirm'
    ),
    url(r'^reset/done/$', views.reset_done_pass,
        name='password_reset_complete'),

    url(r'^forums/$', views.ForumsView.as_view(), name='forums'),
    url(r'^forum/(?P<category>.+)/(?P<forum>.+)/$', views.ForumView.as_view(),
        name='forum'),
    url(
        r'^topic/(?P<category>.+)/(?P<forum>.+)/(?P<slug>[-\w]+)/(?P<idtopic>\d+)/$',
        views.TopicView.as_view(), name='topic'
    ),
    url(
        r'^newtopic/(?P<category>.+)/(?P<forum>.+)/$',
        login_required(views.NewTopicView.as_view()), name='newtopic'
    ),
    url(
        r'^edit_topic/(?P<category>.+)/(?P<forum>.+)/(?P<idtopic>\d+)/$',
        login_required(views.EditTopicView.as_view()), name='edittopic'
    ),
    url(
        r'^delete_topic/$',
        login_required(views.DeleteTopicView.as_view()), name='deletetopic'
    ),
    url(
        r'^open_close_topic/$',
        login_required(views.OpenCloseTopicView.as_view()),
        name="open_close_topic"
    ),
    url(
        r'^like_unlike_topic',
        login_required(views.LikeUnlikeTopicView.as_view()),
        name="like_unlike_topic"
    ),
    url(
        r'^like_unlike_comment',
        login_required(views.LikeUnlikeCommentView.as_view()),
        name="like_unlike_comment"
    ),
    url(
        r'^newcomment/(?P<category>.+)/(?P<forum>.+)/(?P<slug>[-\w]+)/(?P<idtopic>\d+)/$',
        login_required(views.NewCommentView.as_view()), name='newcomment'
    ),
    url(
        r'^updatecomment/(?P<category>.+)/(?P<forum>.+)/(?P<slug>[-\w]+)/(?P<idtopic>\d+)/(?P<idcomment>\d+)/$',
        login_required(views.EditCommentView.as_view()), name='updatecomment'
    ),
    url(
        r'^removecomment/(?P<category>.+)/(?P<forum>.+)/(?P<slug>[-\w]+)/(?P<idtopic>\d+)/(?P<idcomment>\d+)/$',
        login_required(views.DeleteCommentView.as_view()), name='removecomment'
    ),
    url(
        r'^forum_all_notification/$',
        login_required(views.AllNotification.as_view()),
        name='forum_all_notification'
    ),
    url(
        r'^forum_set_notifications/$',
        login_required(views.SetNotifications), name='forum_set_notifications'
    ),
    url(
        r'^new_register/(?P<category>.+)/(?P<forum>.+)/$', login_required(
            views.AddRegisterView.as_view()), name='new_register'
    ),
    url(
        r'^unregister/(?P<category>.+)/(?P<forum>.+)/$', login_required(
            views.UnregisterView.as_view()), name='unregister'
    ),
    url(
        r'^users_forum/(?P<category>.+)/(?P<forum>.+)/$',
        views.UsersForumView.as_view(), name='users_forum'
    ),
    url(
        r'^search_topic/(?P<category>.+)/(?P<forum>.+)/$',
        views.TopicSearch.as_view(), name='search_topic'
    ),
    url(r'^feed/(?P<category>.+)/(?P<forum>.+)/$', TopicFeed(), name='rss'),
    url(
        r'^profile/(?P<username>.+)/$',
        views.ProfileView.as_view(), name='profile'
    ),
    url(
        r'^edit_profile/(?P<username>.+)/$',
        login_required(views.EditProfileView.as_view()), name='edit_profile'
    ),
    url(
        r'profile_is_troll/$',
        login_required(views.IsTrollView.as_view()), name='profile_is_troll'
    ),
]