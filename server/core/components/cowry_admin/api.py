import json, hashlib
from flask import request, Response, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Resource, Api
from service import app, schema, d
from utils import *

api = Api(app)

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
