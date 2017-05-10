import json, hashlib
from flask import request, Response, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from service import app, schema, d
from utils import *


@app.route('/home')
def home():
    return render_template('home/index.html')

@app.route('/home/settings', methods=['POST', 'GET'])
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
