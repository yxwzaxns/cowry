__package__ = 'File'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DefaultClause, Text

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    name = Column(String(50))
    postfix = Column(String(10))
    size = Column(String(30))
    hashcode = Column(String(32))
    updatetime = Column(String(20))
    quotes = Column(Integer(), DefaultClause('0'))
    is_delete = Column(Integer, DefaultClause('0'))
    public = Column(String(1))
    location = Column(String(20))
    # encsize is size of file encrypted
    encsize = Column(String(20))
    # enhashcode is hash of file md5
    enhashcode = Column(String(32))
    # encryption is a token if a file is encrypted
    encryption = Column(Integer(), DefaultClause('0'))
    # type of encryption
    encryption_type = Column(String(20))
    # transfer file Column
    is_transfer = Column(Integer(), DefaultClause('0'))
    transfer_own = Column(String(50), DefaultClause('None'))
    c_enc = Column(Text())

    mysql_charset = 'utf8'

    @property
    def is_open(self):
        if self.public == 1:
            return True
