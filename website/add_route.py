from flask_login import login_required, current_user
from flask import Blueprint, request, make_response
from .models import Driver
from . import db, socket_io


chat = Blueprint('chat', __name__)
connected_drivers = set()
@chat.route("/route", methods=['POST', "DELETE"])
@login_required
def add_route():
    data = request.get_json()
    driver_email = data["driver_email"]
    driver = Driver.query.filter_by(email=driver_email).first()
    
    if driver:
        if request.method == "POST":
            route = data["route"]
            if driver.route != route:  # Check if the route actually changed
                driver.route = route
                db.session.commit()
                if driver.email in connected_drivers:
                    socket_io.emit('route-changed', {"message": "Route changed"}, room=driver.email)
        else:
            driver.route = ""
            db.session.commit()
            if driver.email in connected_drivers:
                socket_io.emit('route-changed', {"message": "Route changed"}, room=driver.email)

        return make_response("Route changed", 200)
    else:
        return make_response("Driver not found", 404)