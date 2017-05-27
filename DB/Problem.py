# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates

from DB.Base import Base


class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    difficulty = Column(Integer,
                        default=0,
                        nullable=False)
    task_type = Column(Integer,
                       default=0,
                       nullable=False)
    # 0 for batch, 1 for interactive, 2 for output only
    active_dataset = Column(Integer, ForeignKey("datasets.id"))

    @validates("difficulty")
    def __validateDifficulty__(self, key, difficulty):
        assert 0 <= difficulty < 101
        return difficulty
