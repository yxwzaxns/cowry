from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Manager(Base):
    __tablename__ = 'manager'

    id = Column(Integer, primary_key=True)
    username = Column(String(10))
    password = Column(String(20))
