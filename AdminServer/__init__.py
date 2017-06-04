"""AdminWebServer implementation."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import os

import tornado.web
from tornado.options import define, options
from AdminServer.handlers import handlers

define('template_path',
       group='application',
       default=os.path.join(os.path.dirname(__file__), "templates"))
define('static_path',
       group='application',
       default=os.path.join(os.path.dirname(__file__), "static"))
define('cookie_secret',
       group='application',
       default="fdsafWDFWREDFADAFWRdFGTEQRGQFGQG")


define("compiled_template_cache",
       group='application',
       default=False)
define("serve_traceback",
       group='application',
       default=True)
define("login_url",
       group='application',
       default="/login")


def make_app():
    """Create tornado app for AdminWebServer."""
    return tornado.web.Application(handlers,
                                   **options.group_dict('application'))
