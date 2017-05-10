from flask import Flask, redirect, url_for, render_template
from flask import send_from_directory
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from flask_sqlalchemy import SQLAlchemy
import hashlib, os
import schema

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static',
            template_folder='views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/aong/workspace/git/cowry/server/db/data/default.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
api = Api(app)

class CowryAdminView(ModelView):
    def is_accessible(self):
        if current_identity:
            return True
        else:
            return False
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

admin = Admin(app, name='Cowry Admin Console', template_mode='bootstrap3')
admin.add_view(CowryAdminView(schema.manager.Manager, db.session))

class HelloWorld(Resource):
    def get(self):
        user = db.session.query(schema.manager.Manager).filter(schema.manager.Manager.username=='aong').first()
        return str(user.__dict__)

    def post(self):
        return render_template('login.html')

api.add_resource(HelloWorld, '/t')

def authenticate(username, password):
    user = db.session.query(schema.manager.Manager).filter(schema.manager.Manager.username==username).first()
    if user and user.username and hashlib.md5(password.encode('utf8')).hexdigest() == user.password:
        return user

def identity(payload):
    user_id = payload['identity']
    user = db.session.query(schema.manager.Manager).filter(schema.manager.Manager.id==user_id).first()
    if user:
        return user.id
    else:
        return None

jwt = JWT(app, authenticate, identity)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/welcome')
@jwt_required()
def echo():
    return redirect('/admin')

@app.route('/images/<path:filename>')
@jwt_required()
def protected(filename):
    return send_from_directory(
        os.path.join(app.instance_path, 'images'), filename
    )
    # return redirect(url_for('images', '1.jpg'))

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
