__doc__ = "this is a db module"
__package__ = 'Db'

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from db import schema

class Db(object):
    """docstring for Db."""
    def __init__(self):
        super(Db, self).__init__()
        # try:
        #
        # except Exception as e:
        #     print(Exception,':', e)
        # else:
        self.engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/cowry', encoding='utf-8', pool_recycle=3600)
        self.Session = sessionmaker(bind = self.engine)
        self.session = self.Session()
    def initDB(self):
        for table in schema.__all__:
            try:
                getattr(schema, table).Base.metadata.create_all(self.engine)
            except Exception as e:
                print(Exception,':', e)



if __name__ == '__main__':
    Db().initDB()
