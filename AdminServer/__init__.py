import os

import tornado.web
from tornado.options import define, options

from AdminServer.handlers.MainHandler import MainHandler
from AdminServer.handlers.LoginHandler import LoginHandler
from AdminServer.handlers.SettingsHandler import SettingsHandler


define('template_path', group='application', default=os.path.join(os.path.dirname(__file__), "templates"))
define('static_path', group='application', default=os.path.join(os.path.dirname(__file__), "static"))
define('cookie_secret', group='application', default="fdsafWDFWREDFADAFWRdFGTEQRGQFGQG")

def make_app ():
    return tornado.web.Application([
        ("/", MainHandler),
        ("/login", LoginHandler),
        ("/settings", SettingsHandler)
        ],
        **options.group_dict('application'))
