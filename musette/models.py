import os

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import models
from django.shortcuts import get_object_or_404
from django.template import defaultfilters
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from . import settings as localSettings
from .validators import valid_extension


@python_2_unicode_compatible
class Category(models.Model):
    """
    Model Category
    """
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
    """
    Model Forum
    """
    idforum = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category, related_name='categories',
        verbose_name=_('Category'), on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self', related_name='parents', verbose_name=_('Parent forum'),
        blank=True, null=True, on_delete=models.CASCADE
    )
    name = models.CharField(_('Name'), max_length=80)
    position = models.IntegerField(_('Position'), blank=True, default=0)
    description = models.TextField(_('Description'), blank=True)
    moderators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='moderators',
        verbose_name=_('Moderators')
    )
    date = models.DateTimeField(
        _('Date'), blank=True, null=True, auto_now_add=True, editable=False
    )
    topics_count = models.IntegerField(
        _('Topics count'), blank=True, default=0, editable=False,
    )
    hidden = models.BooleanField(
        _('Hidden'), blank=False, null=False, default=False,
        help_text=_('If hide the forum in the index page')
    )
    is_moderate = models.BooleanField(
        _('Check topics'), default=False,
        help_text=_('If the forum is moderated')
    )

    class Meta(object):
        unique_together = ('category', 'name', )
        ordering = ['category', 'position', 'name']
        verbose_name = _('Forum')
        verbose_name_plural = _('Forums')

    def __str__(self):
        return self.name

    # Return forums that moderating one moderator
    def tot_forums_moderators(self, moderator):
        tot = self.__class__.objects.filter(
            moderators=moderator
        ).count()

        return tot

    # Add permissions topic to moderator
    def add_permissions_topic_moderator(self, moderator):
        permission1 = Permission.objects.get(codename='add_topic')
        permission2 = Permission.objects.get(codename='change_topic')
        permission3 = Permission.objects.get(codename='delete_topic')

        moderator.user_permissions.add(permission1)
        moderator.user_permissions.add(permission2)
        moderator.user_permissions.add(permission3)

        # Add permission is_staff
        moderator.is_staff = True
        moderator.save()

    # Clear permissions to moderator
    def clear_permissions_moderator(self, moderator):
        moderator.user_permissions.clear()

        # Remove permission is_staff
        moderator.is_staff = False
        moderator.save()

    # Remove permission in user moderators
    def remove_user_permissions_moderator(self):
        for moderator in self.moderators.all():
            # Superuser not is necessary
            if not moderator.is_superuser:
                # Return forums that moderating one moderator
                tot_forum_moderator = self.tot_forums_moderators(moderator)

                # Only remove permissions if is moderator one forum
                if tot_forum_moderator < 1:
                    self.clear_permissions_moderator(moderator)

    def delete(self, *args, **kwargs):
        for moderator in self.moderators.all():
            if not moderator.is_superuser:
                # Only remove permissions if is moderator has one forum
                if self.tot_forums_moderators(moderator) < 1:
                    # Remove permissions to user
                    self.clear_permissions_moderator(moderator)

        super(Forum, self).delete()

    def clean(self):
        if self.name:
            self.name = self.name.strip()

    def forum_description(obj):
        return obj.description
    forum_description.allow_tags = True


class MessageForum(models.Model):
    """
    Message forum model
    """
    idmessage_forum = models.AutoField(primary_key=True)
    forum = models.ForeignKey(
        Forum, related_name='message_information', verbose_name=_('Forum'),
        on_delete=models.CASCADE
    )
    message_information = models.TextField(
        _('Message to inform'), blank=False, null=False,
        help_text=_('If you want to report a message to a forum')
    )
    message_expires_from = models.DateTimeField(
        _('Message expires from'), blank=False, null=False,
        help_text=_('Date from message expired')
    )
    message_expires_to = models.DateTimeField(
        _('Message expires to'), blank=False, null=False,
        help_text=_('Date to message expired')
    )

    class Meta(object):
        verbose_name = _('Message for forums')
        verbose_name_plural = _('Messages for forums')

    def __str__(self):
        return self.message_information


@python_2_unicode_compatible
class Topic(models.Model):
    """
    Model Topic
    """
    def generate_path(instance, filename):
        """
        Generate path to field Attchment
        """
        folder = ""
        folder = "forum_" + str(instance.forum_id)
        folder = folder + "_user_" + str(instance.user)
        folder = folder + "_topic_" + str(instance.id_attachment)
        return os.path.join("forum", folder, filename)

    idtopic = models.AutoField(primary_key=True)
    forum = models.ForeignKey(
        Forum, related_name='forums', verbose_name=_('Forum'),
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='users', verbose_name=_('User'),
        on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100)
    title = models.CharField(_('Title'), max_length=80)
    date = models.DateTimeField(
        _('Date'), blank=False, auto_now=True, db_index=False
    )
    last_activity = models.DateTimeField(
        _('Last activity'), blank=False, auto_now=True, db_index=False
    )
    description = models.TextField(_('Description'), blank=False, null=False)
    id_attachment = models.CharField(max_length=200, null=True, blank=True)
    attachment = models.FileField(
        _('File'), blank=True, null=True, upload_to=generate_path,
        validators=[valid_extension]
    )
    is_close = models.BooleanField(
        _('Closed topic'), default=False,
        help_text=_('If the topic is closed')
    )
    moderate = models.BooleanField(
        _('Moderate'), default=False,
        help_text=_('If the topic is moderated')
    )
    is_top = models.BooleanField(
        _('Top'), default=False,
        help_text=_('If the topic is important and it will go top')
    )
    like = models.PositiveIntegerField(default=0, editable=False)

    class Meta(object):
        ordering = ['forum', 'last_activity', 'title', 'date']
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
        path = media_path + "/" + path_folder

        # Remove attachment if exists
        from .utils import remove_folder, exists_folder
        if exists_folder(path):
            remove_folder(path)

        Topic.objects.filter(idtopic=idtopic).delete()
        self.update_forum_topics(self.forum, "subtraction")

    def save(self, *args, **kwargs):

        if not self.idtopic:
            self.slug = defaultfilters.slugify(self.title)
            self.update_forum_topics(
                self.forum.category.name, self.forum, "sum"
            )

        self.moderate = self.check_topic_moderate()
        self.generate_id_attachment(self.id_attachment)
        super(Topic, self).save(*args, **kwargs)

    def update_forum_topics(self, category, forum, action):

        f = Forum.objects.get(category__name=category, name=forum)
        tot_topics = f.topics_count
        if action == "sum":
            tot_topics = tot_topics + 1
        elif action == "subtraction":
            tot_topics = tot_topics - 1

        Forum.objects.filter(name=forum).update(
            topics_count=tot_topics
        )

    def check_topic_moderate(self):
        """
        Check if one topic is mark like moderate
        """
        # If is superuser
        if self.user.is_superuser:
            return True
        # If the forum not is moderate
        elif not self.forum.is_moderate:
            return True
        # If user is moderator
        elif self.user in self.forum.moderators.all():
            return True
        else:
            return False

    def generate_id_attachment(self, value):
        if not value:
            self.id_attachment = get_random_string(length=32)


@python_2_unicode_compatible
class Comment(models.Model):
    """
    Model Comment
    """

    idcomment = models.AutoField(primary_key=True)
    topic = models.ForeignKey(
        Topic, related_name='topics', verbose_name=_('Topic'),
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='comment_users',
        verbose_name=_('User'), on_delete=models.CASCADE
    )
    date = models.DateTimeField(
        _('Date'), blank=True, auto_now=True, db_index=True
    )
    description = models.TextField(_('Description'), blank=True)
    like = models.PositiveIntegerField(default=0, editable=False)

    class Meta(object):
        ordering = ['date']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return str(self.description)


@python_2_unicode_compatible
class Notification(models.Model):
    """
    Model Notification
    """
    idnotification = models.AutoField(primary_key=True)
    content_type = models.ForeignKey(
        ContentType, null=True, blank=True,
    )
    idobject = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'idobject')
    iduser = models.IntegerField(default=0)
    is_topic = models.BooleanField(default=0)
    is_comment = models.BooleanField(default=0)
    is_view = models.BooleanField(default=0)
    date = models.DateTimeField(blank=True, db_index=True)

    class Meta(object):
        ordering = ['date']

    def __str__(self):
        return str(self.idnotification)


@python_2_unicode_compatible
class LikeTopic(models.Model):
    """
    Model LikeTopic
    """
    topic = models.ForeignKey(
        Topic, related_name='likes_topic', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='likes_topic_users',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.topic.idtopic)


@python_2_unicode_compatible
class LikeComment(models.Model):
    """
    Model LikeComment
    """
    comment = models.ForeignKey(
        Comment, related_name='likes_comment', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='likes_comment_users',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.comment.idcomment)


@python_2_unicode_compatible
class Register(models.Model):
    """
    Model Register
    """
    idregister = models.AutoField(primary_key=True)
    forum = models.ForeignKey(
        Forum, related_name='register_forums', verbose_name=_('Forum'),
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='register_users',
        verbose_name=_('User'), on_delete=models.CASCADE
    )
    date = models.DateTimeField(
        _('Date'), blank=True, auto_now=True, db_index=True
    )

    class Meta(object):
        ordering = ['date']
        verbose_name = _('Register')
        verbose_name_plural = _('Registers')

    def __str__(self):
        return str(self.forum) + " " + str(self.user)


@python_2_unicode_compatible
class AbstractProfile(models.Model):
    """
    Model AbstractProfile
    """
    def generate_path_profile(instance, filename):
        """
        Generate path to field photo
        """
        return os.path.join(
            "profiles", "profile_" + str(instance.iduser_id), filename
        )

    idprofile = models.AutoField(primary_key=True, unique=True)
    iduser = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="user", db_index=True,
        on_delete=models.CASCADE
    )
    photo = models.FileField(
        upload_to=generate_path_profile, null=True, blank=True,
    )
    about = models.TextField(blank=True, null=True)
    activation_key = models.CharField(max_length=100, null=False, blank=False)
    key_expires = models.DateTimeField(auto_now=False)
    is_troll = models.BooleanField(
        _('Is troll'), default=False,
        help_text=_('If the user is troll')
    )

    def __str__(self):
        return str(self.iduser.username)

    def last_seen(self):
        return cache.get('seen_%s' % self.iduser.username)

    def online(self):
        if self.last_seen():
            now = timezone.now()
            if now > self.last_seen() + timezone.timedelta(
                         seconds=localSettings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Configuration(models.Model):
    """
    Model configuration mussete like logo and class css
    """
    def generate_path_configuration(instance, filename):
        """
        Generate path to field logo
        """
        return os.path.join(
            "configuration", filename
        )

    idconfig = models.AutoField(primary_key=True)
    site = models.OneToOneField(Site)
    logo = models.FileField(
        upload_to=generate_path_configuration, null=True, blank=True,
    )
    logo_width = models.PositiveIntegerField(
        _("Logo width"), null=True, blank=True,
        help_text=_('In pixels')
    )
    logo_height = models.PositiveIntegerField(
        _("Logo height"), null=True, blank=True,
        help_text=_('In pixels')
    )
    custom_css = models.TextField(
        _("Custom design"), null=True, blank=True
    )

    class Meta(object):
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')

    def __str__(self):
        return str(self.idconfig)
