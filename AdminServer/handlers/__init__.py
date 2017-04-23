# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from AdminServer.handlers.MainHandler import MainHandler
from AdminServer.handlers.LoginHandler import LoginHandler
from AdminServer.handlers.SettingsHandler import SettingsHandler
from AdminServer.handlers.ContestHandler import ContestHandler

handlers = [
    ("/", MainHandler),
    ("/login", LoginHandler),
    ("/settings", SettingsHandler),
    ("/contest/.+/.*", ContestHandler)
]
