import json, hashlib
from flask import request, Response, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from service import app, schema, d
from utils import *


@app.route('/home')
@login_required
def home():
    print('!!!!!!!{} ^^^ {} !!!!'.format(current_user.is_authenticated, current_user.username))
    return render_template('home/index.html')

@app.route('/home/settings', methods=['POST', 'GET'])
@login_required
@json_response
def settings():
    if request.method == 'POST':
        user = d.session.query(schema.user.User).filter_by(id=current_user.id).first()
        # bob = User.query.filter_by(name='Bob').first()
        user.pubkey = request.form['pubkey'].strip()
        d.session.commit()
        return [request.form['pubkey'].strip()]
    else:
        return current_user.pubkey


@app.route('/register', methods=['POST'])
def register():
    if request.form['password'] == request.form['confirm-password']:
        try:
            d.session.add(schema.user.User(username= request.form['username'],
                                           uuid= generateGUID(),
                                           email= request.form['email'],
                                           password= hashlib.md5(request.form['password'].encode('utf8')).hexdigest()
                                           ))
            d.session.commit()
        except Exception as e:
            error = str(e)
            return redirect(url_for('login', error=error))
        else:
            return redirect('/home')
    else:
        error = 'password not same as confirm-password'
        redirect(url_for('login', error=error))
