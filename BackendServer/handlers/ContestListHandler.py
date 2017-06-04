# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>


from BackendServer.handlers.BaseHandler import BaseHandler

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
from DB.Repositories import ContestRepository


class ContestListHandler(BaseHandler):
    """
    Contests Handler for BackendWebServer.
    """

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("contest_list.html",
                    contests_running=ContestRepository
                    .get_active_contests(self.session),
                    contests_upcoming=ContestRepository
                    .get_future_contests(self.session),
                    contests_recent=ContestRepository
                    .get_recent_contests(self.session))
