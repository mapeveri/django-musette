import base64
import hashlib
import os
import random
import shutil

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
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
    This method verify that exists folder in base to route.

    Args:
        route (str): Path to check if exists.

    Returns:
        bool: Return if exists.
    """
    if os.path.exists(route):
        return True
    else:
        return False


def remove_folder(route_folder):
    """
    This method remove one folder.

    Args:
        route_folder (str): Path folder to remove.
    """
    try:
        shutil.rmtree(route_folder)
    except Exception:
        pass


def remove_file(route_file):
    """
    This method remove one file in base to route and image.

    Args:
        route_file (str): Path file to remove.
    """
    if route_file != "" and route_file is not None:
        if os.path.exists(route_file):
            os.remove(route_file)


def get_folder_attachment(topic):
    """
    This method return the path of one folder attachment for app forum.

    Args:
        topic (obj): Topic object.

    Returns:
        str: Path attachment.
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
    This method remove folder attachment and subtract one topic.

    Args:
        idtopic (int): Identification topic.
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
    This method return the model profile defined by user.
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
    This method get app_label from model instance.

    Args:
        instance (obj): Instance class model.

    Returns:
        str: Name app_label of the model.
    """
    return instance._meta.app_label


def get_count_fields_model(instance):
    """
    This method get count fields from model instance.

    Args:
        instance (obj): instance class model.

    Returns:
        int: Total fields of model.
    """
    return len(instance._meta.fields)


def get_id_profile(iduser):
    """
    This method return one id of model profile.

    Args:
        iduser (int): Identification user.

    Returns:
        obj: Object profile.
    """
    ModelProfile = get_main_model_profile()
    profile = get_object_or_404(ModelProfile, iduser=iduser)

    return profile


def get_users_topic(topic, myuser):
    """
    This method return all users of one topic, else my user.

    Args:
        topic (object): Topic object.
        myuser (int): Identification user logged.

    Returns:
        list(int): List users that commented in the topic.
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
    This method return Notification of one user.

    Args:
        iduser (int): Identification user.

    Returns:
        list(Notification): Notification of user.
    """
    try:
        notif = Notification.objects.filter(
            iduser=iduser).order_by("-date")
    except Notification.DoesNotExist:
        notif = None

    return notif


def get_datetime_topic(date):
    """
    This method return info one datetime for topic or notification.

    Args:
        date (datetime): Datetime topic.

    Returns:
        ste: Time elapsed.
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
    This method return basename of one path.

    Args:
        value (str): Path.

    Returns:
        string: Basename path.
    """
    return os.path.basename(value)


def get_route_file(file_path, file_name):
    """
    This method build the path for a file MEDIA.

    Args:
        file_path (str): File path.
        file_name (str): File name.

    Returns:
        str: Concatenate file path + file name.
    """
    try:
        route_file = file_path + "/" + file_name
    except Exception:
        route_file = ""

    return route_file


def get_photo_profile(iduser):
    """
    This method return photo profile.

    Args:
        iduser (int): Identification user.

    Returns:
        str: Path photo profile.
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
    This method send email for confirm user.

    Args:
        email (str): Email user.
        username (str): Username.
        activation_key (str): Activation Key user.
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


def send_mail_comment(url, list_email):
    """
    Send email comment.

    Args:
        url (str): Url site.
        list_email (list(str): List email to send mail.
    """
    if settings.SITE_URL.endswith("/"):
        site = settings.SITE_URL[:-1]
    else:
        site = settings.SITE_URL

    title_email = _("New comment in %(site)s") % {
        'site': settings.SITE_NAME
    }

    message = _("You have one new comment in the topic: %(site)s") % {
        'site': site + url
    }

    email_from = settings.EMAIL_MUSETTE
    if email_from:
        send_mail(
            title_email, message, email_from,
            list_email, fail_silently=False
        )


def send_mail_topic(email_moderator, forum):
    """
    Send email topic.

    Args:
        email_moderator (str): Email moderator.
        forum (obj): Forum object.
    """
    # Send email to moderator
    if settings.SITE_URL.endswith("/"):
        site = settings.SITE_URL + "forum/" + forum.name
    else:
        site = settings.SITE_URL + "/forum/" + forum.name

    site_name = settings.SITE_NAME
    title_email = _("New topic in %(site)s ") % {'site': site_name}
    message = _("You have one new topic to moderate: %(site)s") % {
        'site': site
    }
    email_from = settings.EMAIL_MUSETTE

    if email_from:
        send_mail(
            title_email, message, email_from,
            [email_moderator], fail_silently=False
        )


def get_data_confirm_email(email):
    """
    This method return info for email confirm.

    Args:
        email (str): Email user.

    Returns:
        dict: Activation key and key expires user.
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
    Check if user is moderator forum.

    Args:
        category (str): Category name.
        forum (obj): Object forum.
        user (obj): Object user.

    Returns:
        bool: If the user is moderator forum.
    """
    forum = get_object_or_404(Forum, category__name=category, name=forum)
    if user in forum.moderators.all():
        return True
    else:
        return False


def user_can_create_topic(category, forum, user):
    """
    Check if user can create topic.

    Args:
        category (str): Category name.
        forum (obj): Object forum.
        user (obj): Object user.

    Returns:
        bool: If the user can create topic.
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
    Get total of forums that moderate one user.

    Args:
        user (obj): Object user.

    Returns:
        int: Total forum that user moderate.
    """
    return Forum.objects.filter(
        moderators=user
    ).count()


def save_notification_model(related_object, idobject, iduser, is_topic):
    """
    Save new notificaiton.

    Args:
        related_object (obj): Object related (Topic or Comment).
        idobject (int): Id object.
        iduser (int): Identification user.
        is_topic (bool): If is a topic.
    """
    if is_topic:
        is_comment = False
    else:
        is_comment = True

    now = timezone.now()
    notification = Notification(
        iduser=iduser, is_view=False,
        idobject=idobject, date=now,
        is_topic=is_topic, is_comment=is_comment,
        content_type=related_object
    )
    notification.save()


def get_moderators_and_send_notification_topic(request, forum, topic):
    """
    Get list moderators to send notification for realtime
    and send notificaiton to model Notification for topic.

    Args:
        request (obj): Object request.
        forum (obj): Object forum.
        topic (obj): Object topic.

    Returns:
        list(int): List users.
    """
    # Get moderators forum
    list_us = []

    related_object = ContentType.objects.get_for_model(topic)
    for moderator in forum.moderators.all():
        # If not is my user
        if moderator.id != request.user.id:
            # Send notification to moderator
            save_notification_model(
                related_object, topic.idtopic, moderator.id, True
            )
            list_us.append(moderator.id)

    return list_us


def get_users_and_send_notification_comment(request, topic, comment):
    """
    Get list users to send notification for realtime
    and send notificaiton to model Notification for comment.

    Args:
        request (obj): Object request.
        forum (obj): Object forum.
        comment (obj): Object comment.

    Returns:
        dict: List users and list_email.
    """
    now = timezone.now()

    myuser = request.user.id
    # Send notifications
    list_us = get_users_topic(topic, myuser)
    list_email = []

    # If not exists user that create topic, add
    user_original_topic = topic.user.id
    user_email = topic.user.email
    comment_user = comment.user.id

    # If the notificacion is mine send to all but not to me
    if user_original_topic == myuser and comment_user == myuser:
        # Not make nothing but list_user is already
        # Not send email
        pass
    # If the notificacion is mine send to all but not to create to comment
    elif user_original_topic == myuser and comment_user != myuser:
        # The user comment not exists in list_us
        # Add user that created topic
        list_us.append(user_original_topic)
        # Add user for send email
        list_email.append(user_email)
    # If the notificacion not is mine send to all but not to me
    elif user_original_topic != myuser and comment_user == myuser:
        # Check if exists the created topic
        if not(user_original_topic in list_us):
            # Send to created topic
            list_us.append(user_original_topic)

        # Add user for send email to created topic
        list_email.append(user_email)
    # If the notificacion not is mine send to all but not to create to comment
    elif user_original_topic != myuser and comment_user != myuser:
        # Check if exists the created topic
        if not(user_original_topic in list_us):
            # Send to created topic
            list_us.append(user_original_topic)

        # Add user for send email to created topic
        list_email.append(user_email)

    # Get content type for comment model
    related_object_type = ContentType.objects.get_for_model(comment)
    for user in list_us:
        save_notification_model(
            related_object_type, comment.idcomment, user, False
        )

    return {
        'list_us': list_us,
        'list_email': list_email
    }


def check_moderate_topic_email(request, forum, obj):
    """
    Check if moderate topic and is moderate send email to moderators.

    Args:
        request (obj): Object request.
        forum (obj): Object forum.
        obj (obj): Object topic.

    Returns:
        obj: Object topic updated.
    """
    # If the forum is moderate
    if forum.is_moderate:
        # If is moderator, so the topic is moderate
        if request.user in forum.moderators.all():
            obj.moderate = True
        elif request.user.is_superuser:
            obj.moderate = True
        else:
            obj.moderate = False

            # Get moderators forum
            for moderator in forum.moderators.all():
                # Send email
                send_mail_topic(moderator.email, forum)
    else:
        obj.moderate = True

    return obj
