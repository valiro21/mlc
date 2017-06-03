# coding=utf-8
"""RootHandler for BackendWebServer."""

from BackendServer.handlers.BaseHandler import BaseHandler

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
from DB.Repositories import ContestRepository, UserRepository,\
    BlogPostRepository


class MainHandler(BaseHandler):
    """Root Handler for BackendWebServer."""

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("main.html",
                    contests_running=ContestRepository
                    .get_active_contests(self.session),
                    contests_upcoming=ContestRepository
                    .get_future_contests(self.session),
                    contests_recent=ContestRepository
                    .get_recent_contests(self.session),
                    most_rated_users=UserRepository
                    .get_most_rated(self.session),
                    recent_blog_posts=BlogPostRepository
                    .get_by_latest_with_username(self.session))
