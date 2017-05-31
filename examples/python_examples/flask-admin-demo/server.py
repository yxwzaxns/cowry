from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Create instnace called app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/position'

# Create SQLAlchemy object
db = SQLAlchemy(app)
