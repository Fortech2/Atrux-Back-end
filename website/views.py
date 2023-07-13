from flask import Blueprint, request, jsonify
from . import db
from .models import User, Driver

views = Blueprint('views', __name__)

@views.route('/')

def home():
    return "gel"

@views.route('/drivers', methods=['POST'])

def drivers():
    data = request.get_json()

    name = data['name']
    email = data['email']
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        return "Denied"
    new_driver = Driver(name = name, user_id = user.id)
    db.session.add(new_driver)
    db.session.commit()
    for i in range(len(user.drivers)):
        print(user.drivers[i].name)
    return "Success"
