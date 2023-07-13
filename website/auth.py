from flask import Blueprint, request, jsonify
from .models import User, Driver
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/login', methods =['GET', 'POST'])

def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user:
        if(check_password_hash(user.password, password)):
            return user.drivers
    return "Failed"


@auth.route('/sign-up', methods=['POST'])

def signup():
    data = request.get_json()

    name = data['name']
    email = data['email'] 
    password = data['password']
    print(name)
    print(email)

    user = User.query.filter_by(email=email).first()
    if user:
        status = "Email already exists"
    elif len(name) < 2: 
        status = "Invalid Name"
    elif len(email) < 5:
        status = "invalid Email"
    else:
        new_user = User(name = name, email = email, password = generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        status = "Accepted"
    return jsonify({"Email" : email, "Name" : name, "Status" : status})


