# coding=utf-8
"""BackendWebServer implementation."""


# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import os

import tornado.web
from tornado.options import define, options

from BackendServer.handlers.RankingHandler import RankingHandler
from BackendServer.handlers.ArchiveHandler import ArchiveHandler
from BackendServer.handlers.MainHandler import MainHandler
from BackendServer.handlers.ProblemHandler import ProblemHandler
from BackendServer.handlers.UserHandler import UserHandler
from BackendServer.handlers.ContestListHandler import ContestListHandler
from BackendServer.handlers.ContestHandler import ContestHandler
from BackendServer.handlers.SubmissionsHandler import SubmissionsHandler
from BackendServer.handlers.RegisterHandler import RegisterHandler


define('template_path',
       group='application',
       default=os.path.join(os.path.dirname(__file__), "templates"))
define('static_path',
       group='application',
       default=os.path.join(os.path.dirname(__file__), "static"))
define("autoreload",
       group='application',
       default=True)
define("debug",
       group='application',
       default=True)
define("compiled_template_cache",
       group='application',
       default=False)
define("serve_traceback",
       group='application',
       default=True)
define('cookie_secret',
       group='application',
       default="fdsafWDFWREDFADAFWRdFGTEQRGQFGQG")


def make_app():
    """Create a Tornado app for BackendWebServer"""
    return tornado.web.Application([
        ("/", MainHandler),
        (r"/archive", ArchiveHandler),
        (r"/ranking", RankingHandler),
        (r"/problem/.+", ProblemHandler),
        (r"/contestlist", ContestListHandler),
        (r"/submissions", SubmissionsHandler),
        (r"/register", RegisterHandler),
        (r"/contest/.+", ContestHandler),
        (r"/user/.+", UserHandler)
        ],
        **options.group_dict('application'))
