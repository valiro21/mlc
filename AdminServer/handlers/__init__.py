# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from AdminServer.handlers.AdminListHandler import AdminListHandler
from AdminServer.handlers.DatasetHandler import DatasetHandler
from AdminServer.handlers.MainHandler import MainHandler
from AdminServer.handlers.LoginHandler import LoginHandler
from AdminServer.handlers.ProblemHandler import ProblemHandler
from AdminServer.handlers.SettingsHandler import SettingsHandler
from AdminServer.handlers.ContestHandler import ContestHandler
from AdminServer.handlers.SubmissionHandler import SubmissionHandler
from AdminServer.handlers.UserSettingsHandler import UserSettingsHandler
from AdminServer.handlers.MonitorHandler import MonitorHandler
from AdminServer.handlers.LogoutHandler import LogoutHandler
from AdminServer.handlers.CreateAdminHandler import CreateAdminHandler
from AdminServer.handlers.EditAdminHandler import EditAdminHandler
from AdminServer.handlers.UserListHandler import UserListHandler
from AdminServer.handlers.CreateUserHandler import CreateUserHandler
from AdminServer.handlers.EditUserHandler import EditUserHandler
from AdminServer.handlers.PostEditorHandler import PostEditorHandler

handlers = [
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/settings", SettingsHandler),
    (r"/monitor", MonitorHandler),
    (r"/contest.*", ContestHandler),
    (r"/problem.*", ProblemHandler),
    (r"/dataset.*", DatasetHandler),
    (r"/user/.+/settings", UserSettingsHandler),
    (r"/admin_list", AdminListHandler),
    (r"/submission/.+", SubmissionHandler),
    (r"/logout", LogoutHandler),
    (r"/create_admin", CreateAdminHandler),
    (r"/edit_admin", EditAdminHandler),
    (r"/user_list", UserListHandler),
    (r"/create_user", CreateUserHandler),
    (r"/edit_user", EditUserHandler),
    (r"/post_editor", PostEditorHandler)
]
