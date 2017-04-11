"""BackendWebServer implementation."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import os

import tornado.web
from tornado.options import define, options

from BackendServer.handlers.MainHandler import MainHandler
from BackendServer.handlers.ProblemHandler import ProblemHandler

define('template_path',
       group='application',
       default=os.path.join(os.path.dirname(__file__), "templates"))
define('static_path',
       group='application',
       default=os.path.join(os.path.dirname(__file__), "static"))


def make_app():
    """Create a Tornado app for BackendWebServer"""
    return tornado.web.Application([
        ("/", MainHandler),
        (r"/problem/.+", ProblemHandler)
        ],
                                    **options.group_dict('application'))
