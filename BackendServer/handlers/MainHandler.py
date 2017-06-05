# coding=utf-8
"""RootHandler for BackendWebServer."""
from tornado.web import HTTPError

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

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Failed to acquire database session.')

        try:
            contests_running = ContestRepository.get_active_contests(session)
            contests_upcoming = ContestRepository.get_future_contests(session)
            contests_recent = ContestRepository.get_recent_contests(session)
            most_rated_users = UserRepository.get_most_rated(session)
            recent_blog_posts = BlogPostRepository\
                .get_by_latest_with_username(session)\

        except:
            raise HTTPError(500, 'A database error has occured.')
        finally:
            session.close()

        self.render("main.html",
                    contests_running=contests_running,
                    contests_upcoming=contests_upcoming,
                    contests_recent=contests_recent,
                    most_rated_users=most_rated_users,
                    recent_blog_posts=recent_blog_posts)
