from flask import Flask
from redis import Redis
from flask_admin import Admin
from flask_admin.contrib import rediscli

app = Flask(__name__)

admin = Admin(app, name='microblog', template_mode='bootstrap3')

admin.add_view(rediscli.RedisCli(Redis(host='localhost',port=6379,db=0)))

app.run(port=8008)
