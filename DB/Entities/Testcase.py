# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
import hashlib

import binascii
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy import LargeBinary

from DB.Entities import Base

def get_digest(obj):
    digest = hashlib.md5(obj).hexdigest()
    return digest.encode()

def get_input_digest(context):
    obj = context.current_parameters['input_file']
    return get_digest(obj)

def get_output_digest(context):
    obj = context.current_parameters['output_file']
    return get_digest(obj)

class Testcase(Base):
    __tablename__ = 'testcases'

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))

    public = Column(Boolean,
                    default=False,
                    nullable=False)  # True public test, False private test
    allow_download = Column(Boolean, default=False, nullable=False)
    codename = Column(String)

    input_file = Column(LargeBinary, nullable=False)
    input_file_digest = Column(LargeBinary,
                               nullable=False,
                               default=get_input_digest,
                               onupdate=get_input_digest
                               )
    output_file = Column(LargeBinary, nullable=False)
    output_file_digest = Column(LargeBinary,
                                nullable=False,
                                default=get_output_digest,
                                onupdate=get_output_digest
                                )

