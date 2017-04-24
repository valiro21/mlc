# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from AdminServer.handlers.MainHandler import MainHandler
from AdminServer.handlers.LoginHandler import LoginHandler
from AdminServer.handlers.ProblemCreateHandler import ProblemCreateHandler
from AdminServer.handlers.SettingsHandler import SettingsHandler
from AdminServer.handlers.ContestHandler import ContestHandler
from AdminServer.handlers.UserSettingsHandler import UserSettingsHandler
from AdminServer.handlers.MonitorHandler import MonitorHandler

handlers = [
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/settings", SettingsHandler),
    (r"/monitor", MonitorHandler),
    (r"/contest/.+/.*", ContestHandler),
    (r"/create/problem", ProblemCreateHandler),
    (r"/user/.+/settings", UserSettingsHandler)
]
