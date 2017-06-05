# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

"""Object model for an a blog post in the DB"""


from sqlalchemy import Column, Integer, String, ForeignKey

from DB.Entities import Base


class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey('admins.id'))  # TODO: index
    title = Column(String)
    body = Column(String)
    created_at = Column(String)
