import json, hashlib
from flask import request, Response, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from service import app, schema, d

@app.route('/')
def index():
    return render_template('index.html')

def valid_login(e, p):
    user = d.session.query(schema.manager.Manager).filter(schema.manager.Manager.email==e).first()
    if user and user.username and hashlib.md5(p.encode('utf8')).hexdigest() == user.password:
        return True
    return False

def get_user(e):
        return d.session.query(schema.manager.Manager).filter(schema.manager.Manager.email==e).first()

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['email'], request.form['password']):
            user = get_user(request.form['email'])
            login_user(user)
            if current_user.is_authenticated:
                next = request.args.get('next')
                return redirect(next or '/admin')
        else:
            error = 'Invalid email/password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/t')
@login_required
def t():
    return 'ok'
