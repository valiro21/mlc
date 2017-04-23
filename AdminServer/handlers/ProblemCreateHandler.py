"""LoginHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from AdminServer.handlers.BaseHandler import BaseHandler


class ProblemCreateHandler(BaseHandler):
    """Handler for login."""
    def data_received(self, chunk):
        pass

    def get(self):
        self.render('problem_create.html')

    def post(self):
        # to do
        self.render('problem_create.html')
        pass
