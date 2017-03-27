#!/usr/bin/python3
from BackendServer import make_app
import tornado.ioloop



if __name__ == "__main__":
    app = make_app ()
    app.listen (8080)
    tornado.ioloop.IOLoop.current().start()
