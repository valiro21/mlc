# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from AdminServer.handlers.AdminListHandler import AdminListHandler
from AdminServer.handlers.MainHandler import MainHandler
from AdminServer.handlers.LoginHandler import LoginHandler
from AdminServer.handlers.ProblemHandler import ProblemHandler
from AdminServer.handlers.SettingsHandler import SettingsHandler
from AdminServer.handlers.ContestHandler import ContestHandler
from AdminServer.handlers.SubmissionHandler import SubmissionHandler
from AdminServer.handlers.UserSettingsHandler import UserSettingsHandler
from AdminServer.handlers.MonitorHandler import MonitorHandler
from AdminServer.handlers.LogoutHandler import LogoutHandler

handlers = [
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/settings", SettingsHandler),
    (r"/monitor", MonitorHandler),
    (r"/contest.*", ContestHandler),
    (r"/problem.*", ProblemHandler),
    (r"/user/.+/settings", UserSettingsHandler),
    (r"/admin_list", AdminListHandler),
    (r"/submission/.+", SubmissionHandler),
    (r"/logout", LogoutHandler)
]
