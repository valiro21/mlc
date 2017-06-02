# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, ARRAY
from sqlalchemy.orm import validates, relationship

from DB.Base import Base
from DB.Dataset import Dataset


class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    contests = relationship("Problem_Contest", back_populates="problem")

    datasets = relationship('Dataset', foreign_keys=[Dataset.problem_id])
    active_dataset_id = Column(Integer, ForeignKey("datasets.id"))
    active_dataset = relationship('Dataset', foreign_keys=[active_dataset_id])

    statement_names = Column(ARRAY(String, zero_indexes=True))
    statements = Column(ARRAY(LargeBinary, zero_indexes=True))

    attachment_names = Column(ARRAY(String, zero_indexes=True))
    attachments = Column(ARRAY(LargeBinary, zero_indexes=True))

    difficulty = Column(Integer,
                        default=0,
                        nullable=False)
    task_type = Column(Integer,
                       default=0,
                       nullable=False)
    # 0 for batch, 1 for interactive, 2 for output only

    @validates("difficulty")
    def __validateDifficulty__(self, key, difficulty):
        assert 0 <= difficulty < 101
        return difficulty
