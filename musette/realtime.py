import json
import redis

from django.conf import settings


def data_base_realtime(obj, photo, forum, username):
    """
    Get data comment for new topic or new comment.

    Args:
        obj (obj): Object topic.
        photo: Photo topic.
        forum (obj): Object forum.
        username (obj): Username user.

    Returns:
        dict: Data base for realtime.
    """
    # Data necessary for realtime
    data = {
        "topic": obj.title,
        "idtopic": obj.idtopic,
        "slug": obj.slug,
        "settings_static": settings.STATIC_URL,
        "username": username,
        "forum": forum,
        "category": obj.forum.category.name,
        "photo": photo
    }

    return data


def new_notification(data_notification, list_us):
    """
    Send new notification topic or comment to redis.

    Args:
        data_notification (list): Data for create a new notification.
        list_us (list(str)): List users to send new notification.
    """
    # Add item for notification
    data_notification['list_us'] = list_us

    # Add to real time new notification
    json_data_notification = json.dumps(data_notification)
    # Redis instance
    r = redis.StrictRedis()
    # Publish
    r.publish('notifications', json_data_notification)


def new_comment(data_comment, comment_description):
    """
    Send new comment.

    Args:
        data_comment (list): Data for create a new comment.
        comment_description (str): Comment description.
    """
    # Publish new comment in topic
    data_comment['description'] = comment_description
    json_data_comment = json.dumps(data_comment)
    # Redis instance
    r = redis.StrictRedis()
    # Publish
    r.publish('comments', json_data_comment)
