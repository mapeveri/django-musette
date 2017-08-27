from urllib.parse import parse_qsl

from channels import Group
from channels.auth import channel_session_user


def get_params(query_string):
    """
    Get first (int) param query string
    """
    params = parse_qsl(query_string)
    return int(params[0][1])


@channel_session_user
def ws_connect_notification(message):
    """Socket connect to notification"""
    user = get_params(message.content['query_string'])
    message.channel_session['user'] = user

    Group("notification-%s" % user).add(message.reply_channel)
    # Accept the connection request
    message.reply_channel.send({"accept": True})


@channel_session_user
def ws_disconnect_notification(message):
    """Socket disconnect to notification"""
    user = message.channel_session['user']
    Group("notification-%s" % user).discard(message.reply_channel)


@channel_session_user
def ws_connect_comment_topic(message):
    """Socket connect to comment topic"""
    topic = get_params(message.content['query_string'])
    message.channel_session['topic'] = topic

    Group("topiccomment-%s" % topic).add(message.reply_channel)
    # Accept the connection request
    message.reply_channel.send({"accept": True})


@channel_session_user
def ws_disconnect_comment_topic(message):
    """Socket disconnect to comment topic"""
    topic = message.channel_session['topic']
    Group("topiccomment-%s" % topic).discard(message.reply_channel)
