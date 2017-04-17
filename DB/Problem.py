# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from DB import Base


class Problem(Base):
    __tableName__ = 'problems'
    id = Column(Integer, primary_key=True)
    problemName = Column(String, unique=True)  # TODO: index
    author = Column(String)
    difficulty = Column(Integer)
    statement = Column(String)

    @validates("difficulty")
    def __validateDifficulty__(self, key, difficulty):
        assert 0 <= difficulty < 101
        return difficulty

    def __repr__(self):
        return "<Problem(problemName='%s', author='%s', difficulty='%s', statement='%s')>" % (
            self.problemName, self.author, self.difficulty, self.statement)
