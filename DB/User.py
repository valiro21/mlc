# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from DB.Base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)  # TODO: index
    firstName = Column(String)
    lastName = Column(String)
    password = Column(String)
    email = Column(String, unique=True)

    @validates("email")
    def __validateEmail__(self, key, email):
        assert '@' in email
        return email

    def __repr__(self):
        return "<User(firstName='%s', lastName='%s', password='%s')>" % (
            self.firstName, self.lastName, self.password)
