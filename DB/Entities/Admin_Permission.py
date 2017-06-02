# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from DB.Entities import Base


class AdminPermission(Base):
    """
    Object model for an admin having a certain permission.
    """

    __tablename__ = 'admin_permissions'

    permission_id = Column(Integer,
                           ForeignKey('permissions.permission_id'),
                           nullable=False)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('permission_id', 'admin_id'),
        {},
    )
