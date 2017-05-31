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
@json_response
def certs():
    cert_path = app.settings.certificates.certificate
    with open(cert_path, 'r') as f:
        cert_file = f.read()
    cert = app.utils.importCert(cert_file)
    cert_digest = cert.digest("sha256")
    cert_signature_algorithm = cert.get_signature_algorithm()
    cert_info = {'cert_digest_{}'.format('sha256'): cert_digest.decode(),
                 'cert_signature_algorithm': cert_signature_algorithm.decode()}
    return cert_info

@app.route('/api/syslog')
@login_required
@json_response
def syslog():
    logs = d.session.query(schema.syslog.Syslog).all()
    res = []
    for l in logs:
        res_t = {}
        for i in l.__dict__:
            res_t[i] = getattr(l, i)
        del res_t['_sa_instance_state']
        res.append(res_t)
    return res, 200
# class Status(Resource):
#     def get(self, item):
#         return {'hello': 'world'}


# api.add_resource(Status, '/api/cert')
# api.add_resource(Status, '/api/user')
# api.add_resource(Status, '/api/status/<string:item>')
