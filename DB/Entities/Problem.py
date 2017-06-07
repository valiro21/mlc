# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import validates, relationship

from DB.Entities import Base


class Problem(Base):
    """
    Object model for the problem entities
    """
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    contests = relationship("Problem_Contest", back_populates="problem")

    # This is for autocomplete, actual attribute gets overwritten
    datasets = None

    active_dataset_id = Column(Integer,
                               ForeignKey("datasets.id", ondelete='SET NULL'))
    active_dataset = relationship('Dataset', foreign_keys=[active_dataset_id])

    statement_names = Column(ARRAY(String, zero_indexes=True), default=[])
    statements = Column(ARRAY(LargeBinary, zero_indexes=True), default=[])

    attachment_names = Column(ARRAY(String, zero_indexes=True), default=[])
    attachments = Column(ARRAY(LargeBinary, zero_indexes=True), default=[])

    difficulty = Column(Integer,
                        default=0,
                        nullable=False)
    task_type = Column(Integer,
                       default=0,
                       nullable=False)

    # 0 for batch, 1 for interactive, 2 for output only

    @staticmethod
    def get_by_contest_id(session):
        pass

    @validates("difficulty")
    def __validateDifficulty__(self, key, difficulty):
        assert 0 <= difficulty < 101
        return difficulty
