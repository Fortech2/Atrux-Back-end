from flask import Blueprint, request, jsonify, make_response
from . import db
from .models import User, Driver
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    return current_user

@views.route('/drivers', methods=['GET'])
@login_required
def get_drivers():
    if isinstance(current_user, Driver):
        return make_response("You are not a dispatcher", 400)
    return current_user.drivers[0].name
