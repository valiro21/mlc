import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.render("main.html")
