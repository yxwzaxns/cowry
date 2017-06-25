from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import schema
from db.seed import seedData
from core.config import Settings
from core import utils

MYSQL_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset={charset}'
SQLITE_URI = 'sqlite:///{dbfile}'

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
        self.tables = schema.__all__
        for t in self.tables:
            setattr(self, t, getattr(getattr(schema, t), t.title()))
        self.initDB()
        self.createSession()

    def initDB(self):
        if self.settings.database.type == 'mysql':
            print('use mysql database')
            import pymysql
            DBURI = MYSQL_URI.format( user= self.settings.database.user,
                                      password= self.settings.database.password,
                                      host= self.settings.database.host,
                                      port= self.settings.database.port,
                                      dbname= self.settings.database.dbname,
                                      charset= self.settings.database.charset)
        elif self.settings.database.type == 'sqlite':
            print('use sqlite database')
            import sqlite3
            DBURI = SQLITE_URI.format(dbfile= self.settings.database.df)
        self.conn = DBURI

    def createSession(self):
        self.engine = create_engine(self.conn, encoding='utf-8', pool_recycle=3600)
        self.Session = sessionmaker(bind = self.engine)
        self.session = self.Session()

    def createTables(self):
        print('start create tables')
        for table in self.tables:
            if not getattr(self, table).__table__.exists(self.engine):
                try:
                    getattr(self, table).metadata.create_all(self.engine)
                except Exception as e:
                    print(Exception,':', e)

    def new(self):
        self.createTables()
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
# the following functions is used to select, update, delete, insert
# and they will return a type of dict result
    # select * from table
    #          ||
    # session.query(file).filter(file.name=='name').first()
    #
    # select(file,(name='name'[,]))
    def select(self, table, ):
        pass

    def update(self, arg):
        pass

    def delate(self, arg):
        pass

    def insert(self, arg):
        pass
