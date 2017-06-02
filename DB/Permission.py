# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

"""Object model for a permission"""


from sqlalchemy import Column, Integer, String
from DB.Base import Base


class Permission(Base):
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True)
    permission_name = Column(String, nullable=False)
