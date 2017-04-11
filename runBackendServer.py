#!/usr/bin/python3

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from BackendServer import make_app
import tornado.ioloop

if __name__ == "__main__":
    __app__ = make_app()
    __app__.listen(8080)
    tornado.ioloop.IOLoop.current().start()
