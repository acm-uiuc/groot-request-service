from flask import Flask, jsonify, request
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

@app.route('/request/', methods=['GET'])
def get_all_requests():
    acm_requests = [r.to_dict() for r in ACMRequest.query.all()]
    return jsonify(acm_requests)

@app.route('/request/<id>/', methods=['GET'])
def get_request(id):
    return jsonify({'acm_request' : ACMRequest.query.get(id).to_dict()})

@app.route('/request/', methods=['POST'])
def post_request():
    print(request.json)
    if not request.json or not 'body' in request.json:
        abort(400)
    acm_request = ACMRequest(request.json['body'])
    db.session.add(acm_request)
    db.session.commit()
    return jsonify({'acm_request' : acm_request.to_dict()})

@app.route('/request/<id>/', methods=['PUT'])
def update_acm_request(id):
    if not request.json:
        abort(400)
    acm_request = ACMRequest.query.get(id)

    if 'body' in request.json:
        acm_request.body = request.json['body']

    if 'completed' in request.json:
        acm_request.set_completed()

    db.session.commit()
    return jsonify({'acm_request' : acm_request.to_dict()})

