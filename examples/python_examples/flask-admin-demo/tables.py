from server import app, db

class User(db.Model):

  __tablename__ = "你好"

  id = db.Column(db.Integer, primary_key=True)
  # name = db.Column(db.String)
  # password = db.Column(db.String)
  # updated_at = db.Column(db.String)
