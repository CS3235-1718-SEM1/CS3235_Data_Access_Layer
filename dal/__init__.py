"""
Data Access Layer abstracts database accesses by exposing a RESTful API
"""
import os
from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres:///cs3235')

db = SQLAlchemy(app)

# Import models only after db is defined so that the DB schema can be properly setup
from . import models


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


@app.route('/students', methods=['GET'])
def get_student():
    # TODO: find a better way to serialize data
    return jsonify({
        'result': [{
            'id': student.id,
            'matric_no': student.matric_no,
            'name': student.name,
            'email': student.email
                   } for student in models.Student.query.all()]
    })


@app.route('/students', methods=['POST'])
def create_student():
    post_data = request.json
    is_successful = True
    try:
        new_student = models.Student(matric_no=post_data['matric_no'], name=post_data['name'], email=post_data['email'])
        db.session.add(new_student)
        db.session.commit()
    except Exception:
        is_successful = False

    return jsonify({
        'is_successful': is_successful
    })
