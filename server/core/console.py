import threading
from core.config import Settings
from core.syslog import Syslog
from core.database import Db
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
db = Db()

admin = Admin(app, name='Cowry Admin', template_mode='bootstrap3')

@app.route('/')
def index():
    return redirect(url_for(''))

class WebConsole(threading.Thread):
    """docstring for WebConsole."""
    def __init__(self):
        super(WebConsole, self).__init__()

        # admin.add_view(ModelView(User, db.session))


    def run(self):
        app.run()
