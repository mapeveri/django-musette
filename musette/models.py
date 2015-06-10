import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from django.template import defaultfilters
from django.utils.encoding import python_2_unicode_compatible
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from .validators import valid_extension

@python_2_unicode_compatible
class Category(models.Model):

	idcategory = models.AutoField(primary_key=True)
	name = models.CharField(max_length=80)
	position = models.IntegerField(blank=True, default=0)
	hidden = models.BooleanField(
		blank=False, null=False, default=False,
		help_text=_('If checked, this category will be visible only for staff')
	)

	class Meta(object):
		ordering = ['position']
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')

	def __str__(self):
		return self.name


@python_2_unicode_compatible
class Forum(models.Model):

	idforum = models.AutoField(primary_key=True)
	category = models.ForeignKey(
		Category, related_name='forums',
		verbose_name=_('Category')
	)
	parent = models.ForeignKey(
		'self', related_name='child_forums', verbose_name=_('Parent forum'),
		blank=True, null=True
	)
	name = models.CharField(_('Name'), max_length=80, unique=True)
	position = models.IntegerField(_('Position'), blank=True, default=0)
	description = models.TextField(_('Description'), blank=True)
	moderators = models.ForeignKey(
		User, blank=True, null=True,
		verbose_name=_('Moderators')
	)
	date = models.DateTimeField(_('Date'), blank=True, null=True)
	topics_count = models.IntegerField(_('Topics count'), blank=True, default=0)
	hidden = models.BooleanField(
		_('Hidden'), blank=False, null=False, default=False
	)
	is_moderate = models.BooleanField(_('Check topics'), default=False)

	class Meta(object):
		ordering = ['category', 'position']
		verbose_name = _('Forum')
		verbose_name_plural = _('Forums')

	def __str__(self):
		return self.name

	def clean(self):
		if self.name:
			self.name = self.name.strip()

	def escape_html_description(obj):
		return obj.description
	escape_html_description.allow_tags = True

def generate_path(instance, filename):

	folder = ""
	folder = "forum_" + str(instance.forum_id)
	folder = folder + "_user_" + str(instance.user)
	folder = folder + "_topic_" + str(instance.id_attachment)
	return os.path.join("forum", folder, filename)


@python_2_unicode_compatible
class Topic(models.Model):

	idtopic = models.AutoField(primary_key=True)
	forum = models.ForeignKey(
		Forum, related_name='topic', verbose_name=_('Forum')
	)
	user = models.ForeignKey(User, related_name='Topic', verbose_name=_('User'))
	slug = models.SlugField(max_length=100)
	title = models.CharField(_('Title'), max_length=80)
	date = models.DateTimeField(_('Date'), blank=False, db_index=False)
	description = models.TextField(_('Description'), blank=False, null=False)
	id_attachment = models.CharField(max_length=200, null=True, blank=True)
	attachment = models.FileField(
		_('File'), blank=True, null=True, upload_to=generate_path,
		validators=[valid_extension]
	)
	moderate = models.BooleanField(_('Moderate'), default=False)

	class Meta(object):
		ordering = ['date', 'title', 'forum']
		verbose_name = _('Topic')
		verbose_name_plural = _('Topics')

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		idtopic = self.idtopic
		forum = self.forum_id

		topic = get_object_or_404(Topic, idtopic=idtopic)

		folder = ""
		folder = "forum_" + str(forum)
		folder = folder + "_user_" + str(topic.user.username)
		folder = folder + "_topic_" + str(topic.id_attachment)
		path_folder = os.path.join("forum", folder)
		media_path = settings.MEDIA_ROOT
		path = media_path + "/" +  path_folder

		# Remove attachment if exists
		from .utils import remove_folder, exists_folder
		if exists_folder(path):
			remove_folder(path)

		Topic.objects.filter(idtopic=idtopic).delete()
		self.update_forum_topics(self.forum, "subtraction")

	def save(self, *args, **kwargs):

		if not self.idtopic:
			self.slug = defaultfilters.slugify(self.title)
			self.update_forum_topics(self.forum, "sum")

		self.generate_id_attachment(self.id_attachment)
		super(Topic, self).save(*args, **kwargs)

	def update_forum_topics(self, forum, action):

		f = Forum.objects.get(name=forum)
		tot_topics = f.topics_count
		if action == "sum":
			tot_topics = tot_topics + 1
		elif action == "subtraction":
			tot_topics = tot_topics - 1

		Forum.objects.filter(name=forum).update(
			topics_count=tot_topics
		)

	def generate_id_attachment(self, value):
		if not value:
			self.id_attachment = get_random_string(length=32)


@python_2_unicode_compatible
class Comment(models.Model):

	idcomment = models.AutoField(primary_key=True)
	topic = models.ForeignKey(
		Topic, related_name='comments', verbose_name=_('Topic')
	)
	user = models.ForeignKey(
		User, related_name='comments', verbose_name=_('User')
	)
	date = models.DateTimeField(_('Date'), blank=True, db_index=True)
	description = models.TextField(_('Description'), blank=True)

	class Meta(object):
		ordering = ['date']
		verbose_name = _('Comment')
		verbose_name_plural = _('Comments')

	def __str__(self):
		return self.date


@python_2_unicode_compatible
class Notification(models.Model):

	idnotification = models.AutoField(primary_key=True)
	idobject = models.IntegerField(default=0)
	iduser = models.IntegerField(default=0)
	is_topic = models.BooleanField(default=0)
	is_comment = models.BooleanField(default=0)
	is_view = models.BooleanField(default=0)
	date = models.DateTimeField(blank=True, db_index=True)

	class Meta(object):
		ordering = ['date']

	def __str__(self):
		return self.date
