import json, hashlib
from flask import request, Response, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from service import app, schema, d
from utils import *
import admin_routes
import user_routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['email'], request.form['password'], request.form['type'].strip()):
            user = get_user(request.form['email'], request.form['type'].strip())
            login_user(user)
            if current_user.is_authenticated:
                next = request.args.get('next')
                if 'manager' == request.form['type'].strip():
                    return redirect(next or '/admin')
                elif 'user' == request.form['type'].strip():
                    return redirect(next or '/home')
                else:
                    return redirect('/')
        else:
            error = 'Invalid email/password'
            return render_template('login.html', error=error)
    user_type = request.args.get('type') or 'user'
    return render_template('login.html', type=user_type)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/t')
@login_required
def t():
    return 'ok'
