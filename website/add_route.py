from flask_login import login_required, current_user
from flask import Blueprint, request, make_response
from .models import Driver
from . import db


chat = Blueprint('chat', __name__)

@chat.route("/route", methods=['POST', "DELETE"])
@login_required
def add_route():
    data = request.get_json()
    driver_email = data["driver_email"]
    driver = Driver.query.filter_by(email=driver_email).first()
    
    if request.method == "POST":
        route = data["route"]
        driver.route = route
    else:
        driver.route = "" 
    db.session.commit()
    return make_response("Route changed", 200)