"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required, create_access_token
import hashlib

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def handle_signup():
    body = request.get_json()
    email = body["email"]
    password = hashlib.sha256(body["password"].encode("utf-8")).hexdigest()
    user = User(email = email, password = password, is_active = True)
    db.session.add(user)
    db.session.commit()
    response_body = {
        "message": "User successfully created"
    }

    return jsonify(response_body), 200

@api.route('/login', methods=['POST'])
def handle_login():
    body = request.get_json()
    email = body["email"]
    password = hashlib.sha256(body["password"].encode("utf-8")).hexdigest()
    user = User.query.filter_by(email = email).first()
    if user and user.password == password:
        access_token = create_access_token(identity = user.id)
        return jsonify(access_token)
    

@api.route('/private', methods=['GET',])
@jwt_required()
def handle_privacy():
    id = get_jwt_identity()
    user = User.query.filter_by(id = id).first()
    

    return jsonify(user.serialize()), 200