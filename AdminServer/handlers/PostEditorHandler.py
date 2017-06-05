# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities.BlogPost import BlogPost
from DB.Entities.Admin import Admin
import datetime
from tornado.web import HTTPError


class PostEditorHandler(BaseHandler):
    def get(self):
        self.render("post_editor.html")

    def post(self):
        title = self.get_argument('post_title', '')
        content = self.get_argument('post_content', '')
        post_time = datetime.datetime.now()

        admin_username = self.get_current_user().decode('utf8')

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire session for database')

        try:
            query = session.query(Admin.id).\
                filter(Admin.username == admin_username).one_or_none()

            admin_id = query[0]
        except:
            raise HTTPError(500, 'Database error')

        content = repr(content)
        content = content[1:]
        content = content[:-1]

        new_post = BlogPost(
            admin_id=admin_id,
            title=title,
            body=content,
            created_at=post_time
        )

        try:
            session.add(new_post)
            session.commit()
        except:
            raise HTTPError(500, 'Database error')

        session.close()
        self.redirect(r"/")