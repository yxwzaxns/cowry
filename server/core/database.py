import sys
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from db import schema
from db.schema import *

class Db(object):
    """docstring for Db."""
    def __init__(self):
        super(Db, self).__init__()
        print('start init server db')
        # try:
        #
        # except Exception as e:
        #     print(Exception,':', e)
        # else:
        self.engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/cowry?charset=utf8', encoding='utf-8', pool_recycle=3600)
        self.Session = sessionmaker(bind = self.engine)
        # self.session = self.Session()

        self.user = user.User
        self.admin = admin.Admin
        self.file = file.File

    def initDB(self):
        for table in schema.__all__:
            try:
                getattr(self, table).metadata.create_all(self.engine)
            except Exception as e:
                print(Exception,':', e)

    def seed(self):
        pass

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
