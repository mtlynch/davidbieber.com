from datetime import datetime
import redis
import tornado.web

MESSAGE_QUEUE = "sendlater:messages"

class SendLaterHandler(tornado.web.RequestHandler):
    def get(self, path="/"):
        self.write("URL: " + path)

class SendLaterMessageHandler(tornado.web.RequestHandler):
    def initialize(self, redis_host="localhost", redis_port=6379):
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    def get(self):
        all_messages = self.redis.lrange(MESSAGE_QUEUE, 0, -1)
        for message in all_messages:
            self.write(message)
            self.write('<br/>\n')

    def post(self):
        message = self.get_argument("message")
        recipient = self.get_argument("recipient")
        sender = self.get_argument("sender")
        when = self.get_argument("when")
        modified = datetime.now()

        self.redis.rpush(MESSAGE_QUEUE, {
            'message': message,
            'sender': sender,
            'recipient': recipient,
            'when': when,
            'modified': modified
        })

handlers = [
    (r'/sendlater/message/?', SendLaterMessageHandler),
    (r'/sendlater/(.*)', SendLaterHandler),
]
