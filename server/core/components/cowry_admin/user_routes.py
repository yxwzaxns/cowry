import json, hashlib
from flask import request, Response, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from service import app, schema, d
from utils import *


@app.route('/home')
@login_required
def home():
    print('!!!!!!!{} ^^^ {} !!!!'.format(current_user.is_authenticated, current_user.username))
    logs = d.session.query(schema.syslog.Syslog).filter_by(uid=current_user.id).all()
    print(current_user.id)
    res = []
    for l in logs:
        res_t = {}
        for i in l.__dict__:
            res_t[i] = getattr(l, i)
        del res_t['_sa_instance_state']
        res.append(res_t)
        print('a',res)
    return render_template('home/index.html', logs= res)

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
