# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
import hashlib

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy import LargeBinary
from sqlalchemy.orm import validates

from DB.Entities import Base


def get_digest(obj):
    digest = hashlib.md5(obj).hexdigest()
    return digest.encode()


class Testcase(Base):
    __tablename__ = 'testcases'

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer,
                        ForeignKey("datasets.id", ondelete='SET NULL'))

    public = Column(Boolean,
                    default=False,
                    nullable=False)  # True public test, False private test
    allow_download = Column(Boolean, default=False, nullable=False)
    codename = Column(String)

    deleted = Column(Boolean, default=False, nullable=False)

    input_file = Column(LargeBinary, nullable=False)
    input_file_digest = Column(LargeBinary,
                               nullable=False)

    output_file = Column(LargeBinary, nullable=False)
    output_file_digest = Column(LargeBinary,
                                nullable=False)

    @validates('input_file')
    def update_input_digest(self, key, input_file):
        self.input_file_digest = get_digest(input_file)
        return input_file

    @validates('output_file')
    def update_output_digest(self, key, output_file):
        self.output_file_digest = get_digest(output_file)
        return output_file
