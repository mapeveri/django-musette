from __future__ import print_function

import json
import threading
from functools import partial

import redis
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

# Client users listener list
clients_notifications = []
clients_comments = []


def redis_listener_notification():
    """
    This method subscribe to redis and send message
    to handler websocket notifications
    """
    r = redis.Redis()
    ps = r.pubsub()
    ps.subscribe('notifications')
    io_loop = tornado.ioloop.IOLoop.instance()

    # Listen notifications
    for message in ps.listen():
        for element in clients_notifications:
            data = json.loads(message['data'].decode("utf-8"))
            if 'list_us' in data:
                users = data['list_us']
                user = int(element.user)
                if user in users:
                    io_loop.add_callback(partial(element.on_message, message))
                else:
                    continue


def redis_listener_comment():
    """
    This method subscribe to redis and send message
    to handler websocket comments
    """
    r = redis.Redis()
    ps = r.pubsub()
    ps.subscribe('comments')
    io_loop = tornado.ioloop.IOLoop.instance()

    # Listen comments
    for message in ps.listen():
        for element in clients_comments:
            data = json.loads(message['data'].decode("utf-8"))
            if 'idtopic' in data:
                idtopic = data['idtopic']
                topic = int(element.topic)
                if topic == idtopic:
                    io_loop.add_callback(partial(element.on_message, message))
                else:
                    continue


class RealtimeHandler(tornado.websocket.WebSocketHandler):
    """
    Handler websocket
    """
    def check_origin(self, origin):
        return True

    def open(self):
        self.user = self.get_argument('user', None)
        self.topic = self.get_argument('topic', None)

        if self.user:
            print('New connection was opened. User: ' + self.user)
            clients_notifications.append(self)
        elif self.topic:
            print('New connection was opened. Topic: ' + self.topic)
            clients_comments.append(self)

    def on_message(self, message):
        self.write_message(message['data'])

    def on_close(self):
        print('Conn closed...')
        if self.user:
            clients_notifications.remove(self)
        elif self.topic:
            clients_comments.remove(self)


# Settings for server tornado
settings = {
    'auto_reload': True,
}

# Routes application tornado
application = tornado.web.Application([
    (r'/ws/', RealtimeHandler),
], **settings)


if __name__ == "__main__":
    # Thread for function redis_listener_notification
    threading.Thread(target=redis_listener_notification).start()
    # Thread for function redis_listener_comment
    threading.Thread(target=redis_listener_comment).start()
    # Run server tornado
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
