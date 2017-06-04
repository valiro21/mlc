# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from BackendServer.ui_methods import dateOf, timeOf
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
        session = self.acquire_sql_session()
        contests_running = ContestRepository.get_active_contests(session)
        contests_upcoming = ContestRepository.get_future_contests(session)
        contests_recent = ContestRepository.get_recent_contests(session)
        session.close()
        self.render("contest_list.html",
                    contests_running=contests_running,
                    contests_upcoming=contests_upcoming,
                    contests_recent=contests_recent,
                    dateOf=dateOf,
                    timeOf=timeOf)
