# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

from sqlalchemy import Column, Integer, String, ForeignKey
from DB.Entities import Base


class RecoveryToken(Base):
    __tablename__ = 'recovery_tokens'

    user_id = Column(Integer,
                     ForeignKey('users.id'))
    recovery_token = Column(String, primary_key=True)
    expiration_date = Column(String, nullable=False, unique=True)
