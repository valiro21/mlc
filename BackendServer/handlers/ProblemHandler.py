import tornado.web
import os


class ProblemHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):

        path_elements = [x for x in self.request.path.split("/") if x]
        problem_id = path_elements[1]

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "statement"))
        if (len(path_elements) >= 4):
            self.redirect("..")

        if path_elements[2] not in ["statement", "submissions", "editorial", "comments"]:
            self.redirect("statement")

        self.render(path_elements[2] + ".html", problem_id=problem_id)
