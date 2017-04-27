import json, hashlib
from functools import wraps
from flask import request, Response, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Resource, Api
from service import app, schema, d

api = Api(app)

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

@app.route('/api')
@login_required
@json_response
def api():
    return "this is api interfacein", 200

@app.route('/api/status')
@login_required
@json_response
def status():
    return [1,2,3,4,5], 200

@app.route('/api/users')
@login_required
@json_response
def users():
    return [1,2,3,4,5], 200

@app.route('/api/certs')
@login_required
@json_response
def certs():
    return [1,2,3,4,5], 200
# class Status(Resource):
#     def get(self, item):
#         return {'hello': 'world'}


# api.add_resource(Status, '/api/cert')
# api.add_resource(Status, '/api/user')
# api.add_resource(Status, '/api/status/<string:item>')
