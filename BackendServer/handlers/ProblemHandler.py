import tornado.web


class ProblemHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        problem_id = [x for x in self.request.path.split("/") if x][1]

        self.render("problem.html", problem_id=problem_id)
