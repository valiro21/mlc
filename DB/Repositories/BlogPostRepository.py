# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from DB.Entities import BlogPost, User


class BlogPostRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(BlogPost).filter(BlogPost.id == id)
        raise ValueError("id must be integer")

    @staticmethod
    def get_by_latest_with_username(session, limit=10):
        return session.query(BlogPost.id,
                             BlogPost.title,
                             BlogPost.body,
                             BlogPost.created_at,
                             User.username)\
            .join(User, BlogPost.user_id == User.id) \
            .limit(limit) \
            .all()
