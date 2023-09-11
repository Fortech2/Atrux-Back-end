import datetime

from flask import Blueprint, request, make_response
from flask_login import login_required

from app import handle_notification
from . import db
from .models import Driver, Root_Notification

chat = Blueprint('chat', __name__)

@chat.route("/route", methods=['POST', "DELETE"])
@login_required
def add_route():
    data = request.get_json()
    driver_email = data["driver_email"]
    driver = Driver.query.filter_by(email=driver_email).first()
    if request.method == "POST":
        route = data["route"]
        now = datetime.datetime.now()
        root_notification = Root_Notification(user_id=driver.id, content=data['route'], expiration=str(f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"))
        driver.route = route
        db.session.add(root_notification)
        db.session.commit()
        handle_notification(driver_email)
    else:
        driver.route = "" 
    db.session.commit()
    return make_response("Route changed", 200)