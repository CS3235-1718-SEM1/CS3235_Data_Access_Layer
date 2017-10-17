"""
Data Access Layer abstracts database accesses by exposing a RESTful API
"""
import os
from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres:///cs3235')
lapi_key = os.getenv('LAPI_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models only after db is defined so that the DB schema can be properly setup
from .models import *
# from .models import db_population # un-comment to populate db

IVLE_LAPI_ROOT_URL = 'https://ivle.nus.edu.sg/api/Lapi.svc'
IVLE_LAPI_ENDPOINTS = {
    'validate_token': IVLE_LAPI_ROOT_URL + '/Validate?APIKey=' + lapi_key + '&Token={auth_token}',
    'get_user_id': IVLE_LAPI_ROOT_URL + '/UserID_Get?APIKey=' + lapi_key + '&Token={auth_token}',
    'get_user_modules': IVLE_LAPI_ROOT_URL + '/Modules?APIKey=' + lapi_key + '&AuthToken={auth_token}'
                                                                             '&Duration=0&IncludeAllInfo=false'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return jsonify({
            'up': True  # the server is up
        })
    else:
        # echo whatever is posted for now
        if request.json is not None:
            return jsonify(request.json)


@app.route('/register_user', methods=['POST'])
def register_user():
    """
    Register the current user to the system
    1. Validate the auth_token
    2. Validate the claimed identity
    3. Get modules
    4. Generate secret_key and send it over
    :return:
    """
    post_data = request.json
    auth_token, ivle_id = post_data['IVLE_auth', 'IVLE_id']

    # Check if the auth_token is legit
    resp = requests.get(IVLE_LAPI_ENDPOINTS['validate_token'].format(auth_token))
    resp_json = resp.json()
    if not resp_json['Success']:
        return jsonify({'success': False}), 401

    # Check if the claimed ivle_id indeed belongs to the user
    resp = requests.get(IVLE_LAPI_ENDPOINTS['get_user_id'].format(auth_token))
    resp_json = resp.json()
    if resp_json != ivle_id:
        return jsonify({'success': False}), 401

    # Get modules this user is taking
    resp = requests.get(IVLE_LAPI_ENDPOINTS['get_user_modules'].format(auth_token))
    resp_json = resp.json()
    module_codes = [module['CourseCode'] for module in resp_json['Results']]

    # Register this user in the system w/ the corresponding modules
    # First check if it exists in the DB
    user_from_db = User.query.filter_by(ivle_id=ivle_id).first()
    if user_from_db is not None:
        return jsonify({'success': False}), 403

    new_user = User(ivle_id=ivle_id)
    for module_code in module_codes:
        module = Module.query.filter_by(code=module_code).first()
        new_user.enrolments.append(module)
    db.session.add(new_user)
    db.session.commit()

    # Add secret_key to User model?
    # Clarify secret_key and OTP generation mechanism

    return jsonify({'success': True, 'secret_key': 'stub'})
