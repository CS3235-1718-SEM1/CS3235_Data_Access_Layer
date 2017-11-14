"""
Data Access Layer abstracts database accesses by exposing a RESTful API
"""
import os
import base64
import pprint
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres:///cs3235')
lapi_key = os.getenv('LAPI_KEY', '')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .helper import *
# Import models only after db is defined so that the DB schema can be properly setup
from .models import *
from .models import db_population
# db_population.populate_module_list()  # uncomment to populate module list
# db_population.populate_rooms()  # uncomment to populate rooms

IVLE_LAPI_ROOT_URL = 'https://ivle.nus.edu.sg/api/Lapi.svc'
IVLE_LAPI_ENDPOINTS = {
    'validate_token': IVLE_LAPI_ROOT_URL + '/Validate?APIKey=' + lapi_key + '&Token={auth_token}',
    'get_user_id': IVLE_LAPI_ROOT_URL + '/UserID_Get?APIKey=' + lapi_key + '&Token={auth_token}',
    'get_user_modules': IVLE_LAPI_ROOT_URL + '/Modules?APIKey=' + lapi_key + '&AuthToken={auth_token}'
                                                                             '&Duration=0&IncludeAllInfo=false'
}
OTP_VALIDATION_TTW = 333333  # time to wait before validating another OTP (in microseconds)


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
    # logging request
    print('The request received for /register_user:')
    pprint.pprint(post_data)
    auth_token, ivle_id = post_data['IVLE_auth'], post_data['IVLE_id']

    # Check if the auth_token is legit
    resp = requests.get(IVLE_LAPI_ENDPOINTS['validate_token'].format(auth_token=auth_token))
    resp_json = resp.json()
    if not resp_json['Success']:
        print('Failed response from IVLE validate auth_token:')
        pprint.pprint(resp_json)
        return jsonify({'success': False}), 401

    # Check if the claimed ivle_id indeed belongs to the user
    resp = requests.get(IVLE_LAPI_ENDPOINTS['get_user_id'].format(auth_token=auth_token))
    resp_json = resp.json()
    if resp_json != ivle_id:
        print('IVLE_ID doesn\'t belong to the user')
        pprint.pprint(resp_json)
        return jsonify({'success': False}), 401

    # Get modules this user is taking
    resp = requests.get(IVLE_LAPI_ENDPOINTS['get_user_modules'].format(auth_token=auth_token))
    resp_json = resp.json()
    module_codes = [module['CourseCode'] for module in resp_json['Results']]
    print('The modules this user is taking:')
    pprint.pprint(module_codes)

    # Register this user in the system w/ the corresponding modules
    # First check if it exists in the DB
    user_from_db = User.query.filter_by(ivle_id=ivle_id).first()
    if user_from_db is not None:
        print('User ' + ivle_id + ' already exists in the DB')
        return jsonify({'success': False}), 403

    random_bytes = os.urandom(24)
    random_base32 = base64.b32encode(random_bytes).decode()

    # Create the user and enrolments in DB
    new_user = User(ivle_id=ivle_id, secret_key=random_base32)
    for module_code in module_codes:
        module = Module.query.filter_by(code=module_code).first()
        if module:
            new_user.enrolments.append(module)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': True, 'secret_key': random_base32})


@app.route('/can_access_door', methods=['POST'])
def can_access_door():
    """
    Check if a particular user can access a room with a specified door_id

    To protect against OTP brute-forcing, for each user this endpoint will only accept 3 guesses per second
    """
    post_data = request.json
    print('The request received for /can_access_door:')
    pprint.pprint(post_data)
    door_id, ivle_id, otp = post_data['door_id'], post_data['IVLE_id'], post_data['otp']

    user = User.query.filter_by(ivle_id=ivle_id).first()
    curr_time = datetime.utcnow()
    time_elapsed = curr_time - user.last_room_access_request_time

    if time_elapsed.total_seconds() < 1 and time_elapsed.microseconds < OTP_VALIDATION_TTW:
        print('Can\'t send too many requests in 1s. Try again in a bit')
        return jsonify({'success': False, 'error': 'Please try the request again after 0.3 second'})

    is_otp_valid, otp_now = validate_otp(user.secret_key, otp)
    user.last_room_access_request_time = curr_time
    db.session.commit()
    if not is_otp_valid:
        print('OTP is invalid. Given: ' + otp + '. Expected: ' + otp_now)
        return jsonify({'success': False}), 400

    room = Room.query.filter_by(door_id=door_id).first()
    for module_taken in user.enrolments:
        if module_taken in room.modules_allowed:
            return jsonify({'result': True, 'success': True})

    print('User has no access to this room')
    return jsonify({'result': False, 'success': True})
