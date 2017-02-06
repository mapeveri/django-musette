import base64
import hashlib
import os
import random
import shutil

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from musette.models import (
    Forum, Topic, Comment, Register,
    Notification, AbstractProfile
)
from musette.email import send_mail


def exists_folder(route):
    """
    This method verify that exists
    folder in base to route
    """
    if os.path.exists(route):
        return True
    else:
        return False


def remove_folder(route_folder):
    """
    This method remove one folder
    """
    try:
        shutil.rmtree(route_folder)
    except Exception:
        pass


def remove_file(route_file):
    """
    This method remove one file
    in base to route and image
    """
    if route_file != "" and not route_file is None:
        if os.path.exists(route_file):
            os.remove(route_file)


def get_folder_attachment(topic):
    """
    This method return the path of one
    folder attachment for app forum
    """
    folder = ""
    folder = "forum_" + str(topic.forum_id)
    folder = folder + "_user_" + str(topic.user.username)
    folder = folder + "_topic_" + str(topic.id_attachment)
    path_folder = os.path.join("forum", folder)
    media_path = settings.MEDIA_ROOT
    path = media_path + "/" + path_folder

    return path


def remove_folder_attachment(idtopic):
    """
    This method remove folder attachment
    and subtract one topic.
    """
    # Subtract one topic
    topic = get_object_or_404(Topic, idtopic=idtopic)
    forum = get_object_or_404(
        Forum, category__name=topic.forum.category.name,
        name=topic.forum, hidden=False
    )
    tot = forum.topics_count
    tot = tot - 1
    Forum.objects.filter(
        category__name=topic.forum.category.name,
        name=topic.forum, hidden=False
    ).update(
        topics_count=tot
    )

    path = get_folder_attachment(topic)

    # Remove attachment if exists
    if exists_folder(path):
        remove_folder(path)


def get_main_model_profile():
    """
    This method return the model profile defined by user
    """
    subclasses = AbstractProfile.__subclasses__()
    if len(subclasses) > 0:
        try:
            return subclasses[0]
        except Exception:
            raise BaseException("Occurs one error to get model profile")
    else:
        raise BaseException("It is not defined profile model")


def get_app_model(instance):
    """
    This method get app_label from model instance
    """
    return instance._meta.app_label


def get_count_fields_model(instance):
    """
    This method get count fields from model instance
    """
    return len(instance._meta.fields)


def get_id_profile(iduser):
    """
    This method return one id of model profile
    """
    ModelProfile = get_main_model_profile()
    profile = get_object_or_404(ModelProfile, iduser=iduser)

    return profile


def get_users_topic(topic, myuser):
    """
    This method return all users of one topic, else my user
    """
    comments = Comment.objects.filter(topic_id=topic.idtopic)
    lista_us = []
    for comment in comments:
        if comment.user_id != myuser:
            if not (comment.user_id in lista_us):
                lista_us.append(comment.user_id)

    return lista_us


def get_notifications(iduser):
    """
    This method return Notification of one user
    """
    try:
        notif = Notification.objects.filter(
            iduser=iduser).order_by("-date")
    except Notification.DoesNotExist:
        notif = None

    return notif


def get_datetime_topic(date):
    """
    This method return info one datetime for topic or notification
    """
    flag = True
    now = timezone.now()
    # If is beteween 1 and 10 return days
    difference = (now - date).days

    # If is this days return hours
    if difference == 0:
        flag = False
        diff = now - date
        minutes = (diff.seconds // 60) % 60
        hours = diff.seconds // 3600
        if minutes < 60 and hours == 0:
            difference = "%s %s" % (
                _("ago"), str((diff.seconds // 60) % 60) + "m ")
        else:
            difference = "%s %s" % (_("ago"), str(diff.seconds // 3600) + "h ")

    # If is days
    if flag:
        difference = "%s %s %s" % (_("ago"), str(difference), _("days ago"))

    return difference


def basename(value):
    """
    This method return basename of one path
    """
    return os.path.basename(value)


def get_route_file(file_path, file_name):
    """
    This method build the path for a file MEDIA
    """
    try:
        route_file = file_path + "/" + file_name
    except Exception:
        route_file = ""

    return route_file


def get_photo_profile(iduser):
    """
    This method return photo profile
    """
    default_photo = static("musette/img/profile.png")
    ModelProfile = get_main_model_profile()
    profile = ModelProfile.objects.filter(iduser=iduser)
    if profile.count() > 0:
        photo = profile[0].photo
        if photo:
            field_photo = settings.MEDIA_URL + str(photo)
        else:
            field_photo = default_photo
    else:
        field_photo = default_photo
    return field_photo


def send_welcome_email(email, username, activation_key):
    """
    This method send email for confirm user
    """
    username = base64.b64encode(username.encode("utf-8")).decode("ascii")
    content = _(
        "Thank you for joining to %(site)s "
        "please enter to confirm your email to this address:"
    ) % {
        'site': settings.SITE_NAME
    }
    urlContent = "confirm_email/" + username + "/" + activation_key
    send_mail(
        _("Welcome to " + settings.SITE_NAME),
        _(content) + settings.SITE_URL + urlContent,
        settings.EMAIL_MUSETTE,
        [email],
        fail_silently=False
    )


def get_data_confirm_email(email):
    """
    This method return info for email confir
    """
    salt = hashlib.sha1(str(random.random()).encode("utf-8")).hexdigest()[:5]
    key = salt.encode("utf-8") + email.encode("utf-8")
    activation_key = hashlib.sha1(key).hexdigest()
    key_expires = timezone.now() + timezone.timedelta(2)

    return {
        'activation_key': activation_key,
        'key_expires': key_expires
    }


def is_user_moderator_forum(category, forum, user):
    """
    Check if user is moderator forum
    """
    forum = get_object_or_404(Forum, category__name=category, name=forum)
    if user in forum.moderators.all():
        return True
    else:
        return False


def user_can_create_topic(category, forum, user):
    """
    Check if user can create topic
    """
    is_moderator = is_user_moderator_forum(category, forum, user)
    is_register = Register.objects.filter(forum=forum, user=user).count()
    # If is superuser or moderator or is register in the forum
    if user.is_superuser or is_moderator or is_register > 0:
        return True
    else:
        return False


def get_total_forum_moderate_user(user):
    """
    Get total of forums that moderate one user
    """
    return Forum.objects.filter(
        moderators=user
    ).count()
