import os, logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from flask_login import LoginManager
import redis

# r = redis.StrictRedis(host='localhost', port=6379, db=0)

# os.sys.path.append(r.get('cowry_root').decode())
from db import schema
from core.config import Settings
from core import utils

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask('cowry_admin',
            static_folder='static',
            static_url_path='/static',
            template_folder='views')

app.settings = Settings()
app.utils = utils
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset={charset}'.format(user='root',
                                                                                                                            # password='1234',
                                                                                                                            # host='125.217.53.144',
                                                                                                                            # port=3306,
                                                                                                                            # dbname='cowry',
                                                                                                                            # charset='utf8')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(app.settings.database.df)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

d = SQLAlchemy(app)
# handler = logging.FileHandler(PROJECT_PATH + '/log/access.log')
# handler.setLevel(logging.DEBUG)
# # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# # handler.setFormatter(formatter)
# app.logger.addHandler(handler)

# @app.before_first_request
# def setup_logging():
#     if not app.debug:
#         # In production mode, add log handler to sys.stderr.
#         handler = logging.FileHandler(PROJECT_PATH + '/log/access.log')
#         app.logger.root.setLevel(logging.DEBUG)
#         app.logger.root.addHandler(handler)

# DSN = 'https://1bc026bce05c42f58aef3a3cc1936293:156a035928b84b648ed1c0e139333c32@sentry.io/159731'
# sentry = Sentry(app, dsn=DSN)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
login_manager.login_message = None

@login_manager.user_loader
def load_user(user_uuid):
    manager = d.session.query(schema.manager.Manager).filter(schema.manager.Manager.uuid==user_uuid).first()
    user = d.session.query(schema.user.User).filter(schema.user.User.uuid==user_uuid).first()
    if user:
        return user
    elif manager:
        return manager
    return None
