# encoding:utf-8
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils import formats, timezone
from django.utils.text import Truncator

from hitcount.models import HitCount

from ..models import Comment, Forum, Topic, Notification
from .photo import get_photo
from ..settings import URL_PROFILE
from ..utils import (
    get_id_profile, get_photo_profile,
    get_datetime_topic, get_params_url_profile
)

register = template.Library()


@register.filter
def in_category(category):
    '''
        This tag filter the forum for category
    '''
    return Forum.objects.filter(
        category_id=category,
        hidden=False
    )


@register.filter
def get_tot_comments(idtopic):
    '''
        This tag filter return the total
        comments of one topic
    '''
    return Comment.objects.filter(
        topic_id=idtopic,
    ).count()


@register.simple_tag
def get_tot_views(idtopic):
    '''
        This tag filter return the total
        views for topic or forum
    '''
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
def get_url_profile(user):
    '''
        Return url of one profile
    '''
    url_profile = URL_PROFILE

    params = get_params_url_profile(user)
    if params:
        url = url_profile + params
    else:
        tag = ""

    return url


@register.filter
def get_path_profile(user):
    '''
        Return tag a with profile
    '''
    url_profile = URL_PROFILE
    username = getattr(user, "username")

    params = get_params_url_profile(user)
    if params:
        tag = "<a href='"+url_profile + params + "'>"+username+"</a>"
    else:
        tag = "<a>"+username+"</a>"

    return tag


@register.filter
def get_tot_users_comments(topic):
    '''
        This tag filter return the total
        users of one topic
    '''
    idtopic = topic.idtopic
    users = Comment.objects.filter(topic_id=idtopic)

    url_profile = URL_PROFILE

    data = ""
    lista = []
    for user in users:
        params_url_profile = get_params_url_profile(user.user)
        usuario = user.user.username
        if not usuario in lista:
            lista.append(usuario)

            photo = get_photo(user.user.id)

            data += "<a href='"+url_profile + params_url_profile + "' >"
            data += "<img class='img-circle' src='"+str(photo)+"' "
            data += "width=30, height=30></a>"

    if len(users) == 0:
        usuario = topic.user.username
        iduser = topic.user.id

        params_url_profile = get_params_url_profile(topic.user)
        photo = get_photo(iduser)
        data += "<a href='"+url_profile + params_url_profile + "'>"
        data += "<img class='img-circle' src='"+str(photo)+"' "
        data += "width=30, height=30></a>"

    return data


@register.filter
def get_tot_topics_moderate(forum):
    '''
        This filter return info about
        Few topics missing for moderate
    '''
    topics_count = forum.topics_count
    idforum = forum.idforum

    moderates = Topic.objects.filter(
        forum_id=idforum,
        moderate=True).count()
    return topics_count - moderates


@register.filter
def get_item_notification(notification):
    '''
        This filter return info about
        one notification of one user
    '''
    idobject = notification.idobject
    is_comment = notification.is_comment

    html = ""
    if is_comment:

        try:
            comment = Comment.objects.get(idcomment=idobject)
            forum = comment.topic.forum.name
            slug = comment.topic.slug
            idtopic = comment.topic.idtopic
            description = Truncator(comment.description).chars(100)
            username = comment.user.username

            url_topic = "/topic/" + forum + "/" + \
                slug + "/" + str(idtopic) + "/"

            title = "<h5><a href='"+url_topic+"'><u>" + \
                comment.topic.title+"</u></h5></a>"

            description = "<p>"+description+"</p>"

            # Get params for url profile
            try:
                params = ""
                params = get_params_url_profile(comment.user)
            except Exception:
                params = ""

            # Data profile
            profile = get_id_profile(comment.user.id)
            photo = get_photo_profile(profile)
            if photo:
                path_img = settings.MEDIA_URL + str(photo)
            else:
                path_img = static("img/profile.png")

            url_profile = URL_PROFILE

            if params:
                user = "<a href='"+url_profile+params + \
                    "'><p>" + username + "</p></a>"
            else:
                user = "<a>" + username + "</a>"

            date = get_datetime_topic(notification.date)

            # Notificacion
            html += '<div class="list-group">'
            html += '   <div class="list-group-item">'
            html += '      <div class="row-action-primary">'
            html += '           <img src="'+path_img + \
                '" width=30 height=30 class="img-circle" />'
            html += '       </div>'
            html += '       <div class="row-content">'
            html += '           <div class="least-content">'+date+'</div>'
            html += '           <h4 class="list-group-item-heading">' + \
                title.encode('utf8')+'</h4>'
            html += '           <p class="list-group-item-text">' + \
                description.encode('utf8')+'</p>'
            html += '           <p>'+user.encode('utf8')+'</p>'
            html += '        </div>'
            html += '   </div>'
            html += '   <div class="list-group-separator"></div>'
            html += '</div>'

        except Comment.DoesNotExist:
            html = ""
    else:
        html = ""

    return html


@register.filter
def get_pending_notifications(user):
    '''
        This method return total pending notifications
    '''
    return Notification.objects.filter(
        is_view=False, iduser=user).count()


@register.filter
def get_last_activity(idtopic):
    '''
        This method return last activity of topic
    '''
    try:
        comment = Comment.objects.filter(
            topic_id=idtopic).order_by("-date")
    except Exception:
        comment = None

    if comment:
        # Get timezone for datetime
        d_timezone = timezone.localtime(comment[0].date)
        # Format data
        date = formats.date_format(d_timezone, "SHORT_DATETIME_FORMAT")

        # Return format data more user with tag <a>
        html = ""
        html += get_path_profile(comment[0].user)
        html += " <p>"+str(date)+"</p>"
        return html
    else:
        topic = Topic.objects.get(idtopic=idtopic)

        # Get timezone for datetime
        d_timezone = timezone.localtime(topic.date)
        # Format data
        date = formats.date_format(d_timezone, "SHORT_DATETIME_FORMAT")

        # Return format data more user with tag <a>
        html = ""
        html += get_path_profile(topic.user)
        html += " <p>"+str(date)+"</p>"
        return html
