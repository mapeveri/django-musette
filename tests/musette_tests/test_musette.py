# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from musette.models import (
	Category, Comment, Forum,
	Notification, Topic
)


class CreateTopicTestCase(TestCase):

	def test_hard_no_more_than(self):
		date = datetime.datetime.now()
		Category.objects.create(
			name="Backend", position=0, hidden=False
		)

		Forum.objects.create(
			category_id=1, parent=None, name="Django",
			position=0, description="Test forum",
			moderators=None, date=date, topics_count=0,
			hidden=False, is_moderate=False
		)

		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		user.last_name = 'Lennon'
		user.save()

		Topic.objects.create(
			forum_id=1, user_id=1, title="test",
			date=date, description="Test topic create",
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
		date = datetime.datetime.now()
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
		date = datetime.datetime.now()
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
