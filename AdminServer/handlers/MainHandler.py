"""MainHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

from AdminServer.handlers import BaseHandler


class MainHandler(BaseHandler.BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("main.html")
