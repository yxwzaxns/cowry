__package__ = 'Manager'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Manager(Base):
    __tablename__ = 'manager'

    id = Column(Integer, primary_key=True)
    username = Column(String(10))
    email = Column(String(10))
    password = Column(String(50))

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
