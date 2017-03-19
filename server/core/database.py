import sys
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from db import schema
from db.schema import *
from db.seed import seedData
from core.config import Settings

class Db(object):
    """docstring for Db."""
    def __init__(self):
        super(Db, self).__init__()
        # try:
        #
        # except Exception as e:
        #     print(Exception,':', e)
        # else:
        self.settings = Settings()
        DBURI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset={charset}'.format(
                                                                                                      user= self.settings.database.user,
                                                                                                      password = self.settings.database.password,
                                                                                                      host = self.settings.database.host,
                                                                                                      port = self.settings.database.port,
                                                                                                      dbname = self.settings.database.dbname,
                                                                                                      charset = self.settings.database.charset)
        self.engine = create_engine(DBURI, encoding='utf-8', pool_recycle=3600)
        self.Session = sessionmaker(bind = self.engine)
        self.session = self.Session()
        self.tables = schema.__all__
        for t in self.tables:
            setattr(self, t, getattr(getattr(schema, t), t.title()))

    def initDB(self):
        for table in self.tables:
            if not getattr(self, table).__table__.exists(self.engine):
                try:
                    getattr(self, table).metadata.create_all(self.engine)
                except Exception as e:
                    print(Exception,':', e)

    def new(self):
        self.initDB()
        self.seed()

    def drop(self):
        for table in self.tables:
            if getattr(self, table).__table__.exists(self.engine):
                try:
                    getattr(self, table).__table__.drop(self.engine)
                except Exception as e:
                    print(Exception,':', e)

    def seed(self):
        self.session.add_all(seedData)
        self.session.commit()
        self.close()

    def close(self):
        self.session.close()

    @staticmethod
    def table(tablename):
        return getattr(self,tablename)

if __name__ == '__main__':
    sys.path.append('./')
    db = Db()
    db.initDB()
    Db.seed()
