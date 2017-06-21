__package__ = 'Manager'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(32))
    username = Column(String(20))
    email = Column(String(50))
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

    @property
    def is_admin(self):
        return True

    def get_id(self):
        return self.uuid
