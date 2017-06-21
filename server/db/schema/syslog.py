__package__ = 'Syslog'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DefaultClause

Base = declarative_base()

class Syslog(Base):
    __tablename__ = 'syslogs'

    id = Column(Integer, primary_key=True)
    uid = Column(String(32))
    ip = Column(String(32))
    event = Column(String(100))
    update_time = Column(String(30))
