from server import app, db
from tables import User
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

app.run()
