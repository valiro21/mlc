import os

import tornado.web
from tornado.options import define, options

from BackendServer.handlers.MainHandler import MainHandler

define('template_path', group='application', default=os.path.join(os.path.dirname(__file__), "templates"))
define('static_path', group='application', default=os.path.join(os.path.dirname(__file__), "static"))

def make_app ():
    return tornado.web.Application([
        ("/", MainHandler)
        ],
        **options.group_dict('application'))
