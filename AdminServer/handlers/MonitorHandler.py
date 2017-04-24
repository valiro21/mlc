"""MonitorHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import tornado

from AdminServer.handlers.BaseHandler import BaseHandler


class MonitorHandler(BaseHandler):
    """SettingsManager for admins."""

    @tornado.web.authenticated
    def get(self):
        self.render("monitor.html", current_archive_setting="Public")
