import tornado

from AdminServer.handlers.BaseHandler import BaseHandler

class SettingsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("settings.html", current_archive_setting="Public")
