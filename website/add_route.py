from flask_login import login_required
from flask import Blueprint, request, make_response
from website.models import Driver
from socketio_manager import socket_io

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
            if driver.route != route:
                driver.route = route
                print(f'Sending route change data: {driver.route} to room {driver_email}')
                socket_io.emit('route-changed', {"route": driver.route}, room=driver_email)
                # Rest of your route update code
        else:
            driver.route = ""
            socket_io.emit('route-changed', {"message": "Route changed"}, room=driver_email)
            # Rest of your route update code

        return make_response("Route changed", 200)
    else:
        return make_response("Driver not found", 404)