from django.db.models import F
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from django.utils import timezone

from musette.models import (
    Category, Comment, Forum, Profile,
    Notification, Topic, Register,
    Configuration
)

from . import utils


class LoginTestCase(TestCase):
    """
    Check login url
    """
    def test_hard_no_more_than(self):
        utils.create_user("admin", "admin@admin.com", "admin123456")
        c = Client()
        response = c.post(reverse_lazy("login"), {
            'username': 'admin', 'password': 'admin123456'
        })
        self.assertTrue(
            response.status_code == 302 or response.status_code == 200
        )


class LogoutTestCase(TestCase):
    """
    Check logout
    """
    def test_logout(self):
        c = Client()
        utils.create_user("admin", "admin@admin.com", "admin123456")
        r = c.login(username='admin', password='admin123456')
        self.assertTrue(r)
        r = c.logout()


class SignupTestCase(TestCase):
    """
    Check signup url
    """
    def test_logout(self):
        now = timezone.now()

        # Create user
        User = get_user_model()
        us = User(
            username="user", email="user@musette.com",
            first_name="User",
            last_name="Musette", is_active=False,
            is_superuser=False, date_joined=now,
            is_staff=False
        )
        us.set_password("user123456")
        us.save()

        c = Client()
        response = c.post(reverse_lazy("login"), {
            'username': 'user', 'password': 'user123456'
        })
        self.assertTrue(
            response.status_code == 302 or response.status_code == 200
        )


class CreateTopicTestCase(TestCase):
    """
    Test create topic
    """
    def test_hard_no_more_than(self):
        date = timezone.now()
        Category.objects.create(
            name="Backend", position=0, hidden=False
        )

        utils.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )

        Forum.objects.create(
            category_id=1, parent=None, name="Django",
            position=0, description="Test forum",
            topics_count=0, hidden=False, is_moderate=False
        )

        Topic.objects.create(
            forum_id=1, user_id=1, title="test",
            date=timezone.now(), description="Test topic create",
            id_attachment="", attachment="", moderate=True
        )


class UpdateTopicTestCase(TestCase):
    """
    Test update topic
    """
    def test_hard_no_more_than(self):
        Topic.objects.filter(
            forum_id=1, user_id=1, idtopic=1
        ).update(description="Test topic update")


class DeleteTopicTestCase(TestCase):
    """
    Test delete topic
    """
    def test_hard_no_more_than(self):
        Topic.objects.filter(
            forum_id=1, user_id=1, idtopic=1
        ).delete()


class NewCommentTopicTestCase(TestCase):
    """
    Test new comment
    """
    def test_hard_no_more_than(self):
        date = timezone.now()
        Comment.objects.create(
            topic_id=1, user_id=1, date=date,
            description="Comment tests"
        )


class EditCommentTopicTestCase(TestCase):
    """
    Test edit comment
    """
    def test_hard_no_more_than(self):
        Comment.objects.filter(
            topic_id=1, user_id=1
        ).update(description="Comment test update")


class DeleteCommentTopicTestCase(TestCase):
    """
    Test delete comment
    """
    def test_hard_no_more_than(self):
        Comment.objects.filter(
            topic_id=1, user_id=1
        ).delete()


class NewNotificationTopicTestCase(TestCase):
    """
    Test new notification
    """
    def test_hard_no_more_than(self):
        date = timezone.now()
        Notification.objects.create(
            idobject=1, iduser=1, date=date,
            is_topic=False, is_comment=True,
            is_view=False
        )


class EditNotificationTopicTestCase(TestCase):
    """
    Test edit notification
    """
    def test_hard_no_more_than(self):
        Notification.objects.filter(
            idobject=1, iduser=1,
            is_topic=False, is_comment=True
        ).update(is_view=True)


class DeleteNotificationTopicTestCase(TestCase):
    """
    Test delete notification
    """
    def test_hard_no_more_than(self):
        Notification.objects.filter(
            idobject=1, iduser=1,
            is_topic=False, is_comment=True
        ).delete()


class AddRegisterTestCase(TestCase):
    """
    Test add register to forum
    """
    def test_hard_no_more_than(self):
        Register.objects.create(
            user_id=1, date=timezone.now(), forum_id=1
        )


class UnRegisterTopicTestCase(TestCase):
    """
    Test Unregister to forum
    """
    def test_hard_no_more_than(self):
        Register.objects.filter(
            user_id=1, forum_id=1,
        ).delete()


class LikeTopicTestCase(TestCase):
    """
    Test like topic
    """
    def test_hard_no_more_than(self):
        Topic.objects.filter(idtopic=1).update(
            like=F('like') + 1
        )


class UnLikeTopicTestCase(TestCase):
    """
    Test Unlike topic
    """
    def test_hard_no_more_than(self):
        Topic.objects.filter(idtopic=1).update(
            like=F('like') - 1
        )


class IsTrollTestCase(TestCase):
    """
    Test Check user is troll
    """
    def test_hard_no_more_than(self):
        # Get troll
        utils.create_user(
            "userexample", "userexample@admin.com", "userexample123456"
        )
        User = get_user_model()
        username = get_object_or_404(User, username="userexample")

        total = Forum.objects.filter(
            moderators=username
        ).count()

        # Check if is user correct
        if not username.is_superuser and total == 0:
            # Is a troll
            Profile.objects.filter(
                iduser=username
            ).update(is_troll=True)


class EditProfileTestCase(TestCase):
    """
    Test Edit profile
    """
    def test_hard_no_more_than(self):
        utils.create_user(
            "userexample", "userexample@admin.com", "userexample123456"
        )
        User = get_user_model()
        username = get_object_or_404(User, username="userexample")
        Profile.objects.filter(iduser=username).update(
            photo="", about="Example about", location="this.location",
            activation_key="", key_expires=timezone.now(),
            is_troll=False, receive_emails=True
        )


class ConfigurationTestCase(TestCase):
    """
    Test configuration
    """
    def test_hard_no_more_than(self):
        mysite = Site.objects.get_current()
        mysite.domain = 'mysite.com'
        mysite.name = 'My Site'
        mysite.save()

        Configuration.objects.create(
            site=mysite, logo=None, favicon=None,
            logo_width=200, logo_height=200, custom_css="",
            description="Test", keywords="test, django"
        )
