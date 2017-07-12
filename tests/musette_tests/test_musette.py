from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from musette.models import (
    Category, Comment, Forum, Profile,
    Notification, Topic, Register
)


class CreateTopicTestCase(TestCase):

    def test_hard_no_more_than(self):
        date = timezone.now()
        Category.objects.create(
            name="Backend", position=0, hidden=False
        )

        User = get_user_model()
        user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        user.last_name = 'Lennon'
        user.save()

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

    def test_hard_no_more_than(self):
        Topic.objects.filter(
            forum_id=1, user_id=1, idtopic=1
        ).update(description="Test topic update")


class DeleteTopicTestCase(TestCase):

    def test_hard_no_more_than(self):
        Topic.objects.filter(
            forum_id=1, user_id=1, idtopic=1
        ).delete()


class NewCommentTopicTestCase(TestCase):

    def test_hard_no_more_than(self):
        date = timezone.now()
        Comment.objects.create(
            topic_id=1, user_id=1, date=date,
            description="Comment tests"
        )


class EditCommentTopicTestCase(TestCase):

    def test_hard_no_more_than(self):
        Comment.objects.filter(
            topic_id=1, user_id=1
        ).update(description="Comment test update")


class DeleteCommentTopicTestCase(TestCase):

    def test_hard_no_more_than(self):
        Comment.objects.filter(
            topic_id=1, user_id=1
        ).delete()


class NewNotificationTopicTestCase(TestCase):

    def test_hard_no_more_than(self):
        date = timezone.now()
        Notification.objects.create(
            idobject=1, iduser=1, date=date,
            is_topic=False, is_comment=True,
            is_view=False
        )


class EditNotificationTopicTestCase(TestCase):

    def test_hard_no_more_than(self):
        Notification.objects.filter(
            idobject=1, iduser=1,
            is_topic=False, is_comment=True
        ).update(is_view=True)


class DeleteNotificationTopicTestCase(TestCase):

    def test_hard_no_more_than(self):
        Notification.objects.filter(
            idobject=1, iduser=1,
            is_topic=False, is_comment=True
        ).delete()


class AddRegisterTestCase(TestCase):

    def test_hard_no_more_than(self):
        Register.objects.create(
            user_id=1, date=timezone.now(), forum_id=1
        )


class DeleteNotificationTopicTestCase(TestCase):

    def test_hard_no_more_than(self):
        Register.objects.filter(
            user_id=1, forum_id=1,
        ).delete()
