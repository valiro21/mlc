from AdminServer.handlers import BaseHandler


class MainHandler(BaseHandler.BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("main.html")
