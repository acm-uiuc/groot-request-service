from flask import Flask, jsonify, request, abort
from models import db, ACMRequest
from settings import MYSQL
from sqlalchemy.sql.expression import func, text
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    MYSQL['user'],
    MYSQL['password'],
    MYSQL['host'],
    MYSQL['dbname']
)

db.init_app(app)
db.create_all(app=app)

@app.route('/request', methods=['GET'])
def get_all_acm_requests():
    acm_requests = [r.to_dict() for r in ACMRequest.query.all()]
    return jsonify(acm_requests)

@app.route('/request/<id>', methods=['GET'])
def get_acm_request(id):
    acm_request = ACMRequest.query.get(id)
    if acm_request == None:
        abort(404)
        
    return jsonify({'acm_request' : acm_request.to_dict()})

@app.route('/request', methods=['POST'])
def post_acm_request():
    if not request.json or not 'body' in request.json:
        abort(400)

    acm_request = ACMRequest(request.json['body'])

    db.session.add(acm_request)
    db.session.commit()

    return jsonify({'acm_request' : acm_request.to_dict()})

@app.route('/request/<id>', methods=['PUT'])
def update_acm_request(id):
    if not request.json:
        abort(400)

    acm_request = ACMRequest.query.get(id)

    if acm_request == None:
        abort(404)

    if 'body' in request.json:
        acm_request.body = request.json['body']

    if 'completed' in request.json:
        acm_request.completed = request.json['completed']

    db.session.commit()
    return jsonify({'acm_request' : acm_request.to_dict()})

