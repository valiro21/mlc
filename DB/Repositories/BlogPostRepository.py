# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from DB.Entities import BlogPost, Admin


class BlogPostRepository:
    @staticmethod
    def get_by_id(session, id):
        """
        Gets a BlogPost with the specified id
        :param session:
        :param id:
        :return: a BlogPost entity
        """
        if isinstance(id, int):
            return session.query(BlogPost).filter(BlogPost.id == id).one()
        raise ValueError("id must be integer")

    @staticmethod
    def get_by_latest_with_username(session, limit=10):
        """
        Geta a list with all the lated BlogPosts
        :param session:
        :param limit: The number of BlogPosts returned
        :return: a list of BlogPosts
        """
        return session.query(BlogPost.id,
                             BlogPost.title,
                             BlogPost.body,
                             BlogPost.created_at,
                             Admin.username)\
            .join(Admin, BlogPost.admin_id == Admin.id)\
            .order_by(BlogPost.created_at.desc())\
            .limit(limit)\
            .all()
