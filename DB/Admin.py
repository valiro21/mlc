# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

"""Object model for an Admin in the DB"""


from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import validates

from DB.Base import Base


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)  # TODO: index
    firstName = Column(String)
    lastName = Column(String)
    password = Column(String)
    avatar = Column(LargeBinary)
    email = Column(String, unique=True)

    @validates("email")
    def __validateEmail__(self, key, email):
        assert '@' in email
        return email
