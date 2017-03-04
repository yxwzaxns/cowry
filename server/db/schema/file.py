__package__ = 'File'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    name = Column(String(20))
    size = Column(String(20))
    updatetime = Column(String(20))
    postfix = Column(String(20))
