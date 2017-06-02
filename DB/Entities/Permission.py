# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

"""Object model for a permission"""


from sqlalchemy import Column, Integer, String
from DB.Entities import Base


class Permission(Base):
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True)
    permission_name = Column(String, nullable=False, unique=True)
