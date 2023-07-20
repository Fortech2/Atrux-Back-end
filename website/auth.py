from flask import Blueprint, request, jsonify, make_response, json
from .models import Dispatcher, Driver
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.dialects.postgresql import insert

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = Dispatcher.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return make_response("You logged in successfully", 200)
    driver = Driver.query.filter_by(email=email).first()
    if driver:
        if check_password_hash(driver.password, password):
            login_user(driver, remember=True)
            return make_response("You logged in successfully", 200)

    return make_response("Failed", 500)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return make_response("logout complete", 200)


@auth.route('/sign-up', methods=['POST'])
def signup():
    data = request.get_json()

    role = data['role']
    name = data['name']
    email = data['email']
    password = data['password']
    phone_number = data['phone_number']

    driver = Driver.query.filter_by(email=email).first()
    user = Dispatcher.query.filter_by(email=email).first()
    if user or driver:
        return make_response("Email already exists", 400)
    else:
        match role:
            case "driver":
                dispatcher = Dispatcher.query.filter_by(phone_number=phone_number).first()
                if dispatcher is None: 
                    return make_response("Dispatcher not found", 404)
                new_driver = Driver(name=name, email=email, password=generate_password_hash(password, method='sha256'),
                                    dispatcher_id=dispatcher.id)
                db.session.add(new_driver)
                db.session.commit()
            case "dispatcher":
                new_user = Dispatcher(name=name, email=email, password=generate_password_hash(password, method='sha256'),
                                phone_number=phone_number)
                db.session.add(new_user)
                db.session.commit()
        return make_response(jsonify({"Email": email, "Name": name}), 200)

@auth.route('/profile', methods=['PUT'])
@login_required
def edit_profile():
    data = request.get_json()
    email = data['email']
    name = data['name']
    phone_number = data['phone_number']

    if email:
        current_user.email = email
    if name:
        current_user.name = name
    if phone_number:
        current_user.phone_number = phone_number 
    db.session.commit()
    return make_response("Data changed", 200)


@auth.route('/driver', methods=['PUT'])
def remove_driver():
        if isinstance(current_user, Driver):
            return make_response("You are not a dispatcher", 401)
        data = request.get_json()
        id = data['id']
        driver = Driver.query.filter_by(id=id).first()
        driver.dispatcher_id = "Marinel"
        return make_response('Driver removed', 200)
