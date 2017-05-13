import json, hashlib, uuid
from functools import wraps
from flask import request, Response, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from service import app, schema, d

def valid_login(e, p, type='user'):
    print('########valid_login',e,p,type)
    if type == 'manager':
        user = d.session.query(schema.manager.Manager).filter(schema.manager.Manager.email==e).first()
        print(1,user)
        if user and user.username and hashlib.md5(p.encode('utf8')).hexdigest() == user.password:
            return True
    elif type == 'user':
        user = d.session.query(schema.user.User).filter(schema.user.User.email==e).first()
        print(2,user)
        if user and user.username and hashlib.md5(p.encode('utf8')).hexdigest() == user.password:
            return True
    return False

def generateGUID():
    return uuid.uuid1().hex.upper()

def get_user(e, type='manager'):
        if type == 'manager':
            return d.session.query(schema.manager.Manager).filter(schema.manager.Manager.email==e).first()
        else:
            return d.session.query(schema.user.User).filter(schema.user.User.email==e).first()

def json_response(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response_code = 200
        response_headers = dict()
        if isinstance(response, dict) or isinstance(response, list):
            response_body = json.dumps(response, indent=4)
        elif isinstance(response, tuple):
            if len(response) == 2:
                response_body, response_code = response
            else:
                response_body, response_code, response_headers = response

            response_body = json.dumps(response_body, indent=4)
        else:
            response_body = response

        return Response(response=response_body, status=response_code,
                        headers=response_headers, mimetype='application/json')


    return wrapper
