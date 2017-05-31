from service import app, schema, d
import os.path as op
from redis import Redis
from flask import redirect, url_for, request
from flask_admin.contrib import rediscli
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from flask_login import current_user, login_required

import routes
import api


class DbView(ModelView):
    def is_accessible(self):
        if hasattr(current_user, 'is_admin') and current_user.is_admin == 1:
            return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url, type='manager'))

class FilesModelView(DbView):
    column_list = ('id', 'uid', 'postfix', 'encryption_type', 'encsize', 'updatetime', 'size', 'name', 'encryption', 'public', 'hashcode','is_delete')

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        if not hasattr(current_user, 'is_admin') or current_user.is_admin != 1:
            return redirect(url_for('login', next=request.url, type='manager'))
        return super(MyAdminIndexView, self).index()

admin = Admin(app, name='Cowry Admin Console', index_view=MyAdminIndexView(), template_mode='bootstrap3', )
admin.add_view(DbView(schema.manager.Manager, d.session))
admin.add_view(DbView(schema.user.User, d.session))
admin.add_view(FilesModelView(schema.file.File, d.session))
admin.add_view(DbView(schema.syslog.Syslog, d.session))
admin.add_view(rediscli.RedisCli(Redis()))

# path = op.join(op.dirname(__file__), 'static')
# admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

if __name__ == '__main__':
    app.run(port=8000)
