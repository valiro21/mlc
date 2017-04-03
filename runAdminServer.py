#!/usr/bin/python3
from AdminServer import make_app
import tornado.ioloop

if __name__ == "__main__":
    app = make_app ()
    app.listen (8081)
    tornado.ioloop.IOLoop.current().start()
