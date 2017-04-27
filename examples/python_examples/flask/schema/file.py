from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    name = Column(String(20))
    size = Column(String(20))
    # encsize is size of file encrypted
    encsize = Column(String(20))
    # encryption is a token if a file is encrypted
    encryption = Column(String(1))
    # type of encryption
    encryption_type = Column(String(20))
    hashcode = Column(String(32))
    updatetime = Column(String(20))
    postfix = Column(String(20))

    mysql_charset = 'utf8'
