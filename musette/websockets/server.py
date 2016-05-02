from __future__ import print_function

import threading
from functools import partial

import redis
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket


LISTENERS = []


def redis_listener():
    r = redis.Redis()
    ps = r.pubsub()
    ps.subscribe('notifications')
    io_loop = tornado.ioloop.IOLoop.instance()
    for message in ps.listen():
        for element in LISTENERS:
            io_loop.add_callback(partial(element.on_message, message))


class RealtimeHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print('New connection was opened')
        LISTENERS.append(self)

    def on_message(self, message):
        self.write_message(message['data'])

    def on_close(self):
        print('Conn closed...')
        LISTENERS.remove(self)


settings = {
    'auto_reload': True,
}

application = tornado.web.Application([
    (r'/ws/', RealtimeHandler),
], **settings)


if __name__ == "__main__":
    threading.Thread(target=redis_listener).start()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()