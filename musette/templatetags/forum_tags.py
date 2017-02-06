from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.utils import formats, timezone

from hitcount.models import HitCount

from ..models import Comment, Forum, Topic, Notification
from .photo import get_photo
from ..utils import (
    get_photo_profile, get_datetime_topic,
    get_total_forum_moderate_user
)

register = template.Library()


@register.filter
def in_category(category):
    """
    This tag filter the forum for category
    """
    return Forum.objects.filter(
        category_id=category,
        hidden=False
    )


@register.filter
def get_tot_comments(idtopic):
    """
    This tag filter return the total
    comments of one topic
    """
    return Comment.objects.filter(
        topic_id=idtopic,
    ).count()


@register.simple_tag
def get_tot_views(idtopic):
    """
    This tag filter return the total
    views for topic or forum
    """
    try:
        content = Topic.objects.get(idtopic=idtopic)
        idobj = ContentType.objects.get_for_model(content)

        hit = HitCount.objects.get(
            object_pk=idtopic,
            content_type_id=idobj
        )
        total = hit.hits
    except Exception:
        total = 0

    return total


@register.filter
def get_path_profile(user):
    """
    Return tag a with profile
    """
    username = getattr(user, "username")
    url = str(reverse_lazy("profile", kwargs={'username': username}))
    tag = "<a href='" + url + "'>" + username + " </a>"

    return tag


@register.filter
def get_tot_users_comments(topic):
    """
    This tag filter return the total
    users of one topic
    """
    idtopic = topic.idtopic
    users = Comment.objects.filter(topic_id=idtopic)

    data = ""
    lista = []
    for user in users:
        username = user.user.username
        url = str(reverse_lazy("profile", kwargs={'username': username}))

        if not (username in lista):
            lista.append(username)

            photo = get_photo(user.user.id)

            tooltip = "data-toggle='tooltip' data-placement='bottom' "
            tooltip += "title='" + username + "'"
            data += "<a href='" + url + "' " + tooltip + ">"
            data += "<img class='img-circle' src='" + str(photo) + "' "
            data += "width=30, height=30></a>"

    if len(users) == 0:
        username = topic.user.username
        url = str(reverse_lazy("profile", kwargs={'username': username}))
        iduser = topic.user.id

        photo = get_photo(iduser)
        data += "<a href='" + url + "'>"
        data += "<img class='img-circle' src='" + str(photo) + "' "
        data += "width=30, height=30></a>"

    return data


@register.filter
def get_tot_topics_moderate(forum):
    """
    This filter return info about
    Few topics missing for moderate
    """
    topics_count = forum.topics_count
    idforum = forum.idforum

    moderates = Topic.objects.filter(
        forum_id=idforum,
        moderate=True).count()
    return topics_count - moderates


@register.filter
def get_item_notification(notification):
    """
    This filter return info about
    one notification of one user
    """
    idobject = notification.idobject
    is_comment = notification.is_comment

    html = ""
    try:
        # If is comment notification
        if is_comment:
            comment = Comment.objects.get(idcomment=idobject)
            forum = comment.topic.forum.name
            category = comment.topic.forum.category.name
            slug = comment.topic.slug
            idtopic = comment.topic.idtopic
            username = comment.user.username
            title = comment.topic.title
            userid = comment.user.id
        else:
            # Is topic notification
            topic = Topic.objects.get(idtopic=idobject)
            forum = topic.forum.name
            category = topic.forum.category.name
            slug = topic.slug
            idtopic = topic.idtopic
            username = topic.user.username
            title = topic.title
            userid = topic.user.id

        url_topic = str(reverse_lazy("topic", kwargs={
            'category': category, 'forum': forum,
            'slug': slug, 'idtopic': idtopic
        }))
        title = "<h5><a href='" + url_topic + "'><u>" + title + "</u></a></h5>"

        # Data profile
        photo = get_photo_profile(userid)
        date = get_datetime_topic(notification.date)
        url_profile = str(reverse_lazy("profile", kwargs={'username': username}))

        # Notificacion
        html += '<a class="content" href="' + url_topic + '">'
        html += ' <h4 class="item-title">'
        html += ' <img class="img-circle pull-left" src="' + photo + '"'
        html += ' width=45 height=45 />'
        html += title + '</h4>'
        html += ' <p class="item-info"><a href="' + url_profile + '">'
        html += username + "</a> - " + str(date)
        html += '</p></a>'
    except Comment.DoesNotExist:
        html = ""

    return html


@register.filter
def get_pending_notifications(user):
    """
    This method return total pending notifications
    """
    return Notification.objects.filter(
        is_view=False, iduser=user).count()


@register.filter
def get_last_activity(topic):
    """
    This method return last activity of topic
    """
    # Get timezone for datetime
    d_timezone = timezone.localtime(topic.last_activity)
    # Format data
    date = formats.date_format(d_timezone, "SHORT_DATETIME_FORMAT")

    # Return format data more user with tag <a>
    html = ""
    # html += get_path_profile(topic.user)
    html += " <p>" + str(date) + "</p>"
    return html


@register.filter
def get_object_user(obj, user):
    """
    Get object user
    """
    if obj:
        return user.user
    else:
        return user


@register.filter
def get_tot_users_forum(forum):
    """
    Get total users register and moderators
    """
    users_registers = forum.register_forums.all().count()
    moderators = forum.moderators.all().count()
    return users_registers + moderators


@register.filter
def check_like_comment(comment, user):
    """
    Check if like comment is checked
    """
    return user.likes_comment_users.filter(
        user=user, comment=comment
    ).count() == 0


@register.filter
def check_like_topic(topic, user):
    """
    Check if like topic is checked
    """
    return user.likes_topic_users.filter(
        user=user, topic=topic
    ).count() == 0


@register.filter
def get_total_forum_moderator(user):
    """
    Get total of forums that moderate one user
    """
    return get_total_forum_moderate_user(user)
