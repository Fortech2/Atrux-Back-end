from flask_socketio import SocketIO
from website.models import Driver


socket_io = SocketIO(cors_allowed_origins="*")

def get_driver_email_by_id(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        return driver.email
    return None

@socket_io.on('connect')
def handle_connect(driver_id):
    driver_email = get_driver_email_by_id(driver_id)
    if driver_email:
        socket_io.join_room(driver_email)
        print(f'Driver {driver_email} connected')

@socket_io.on('disconnect')
def handle_disconnect(driver_id):
    driver_email = get_driver_email_by_id(driver_id)
    if driver_email:
        socket_io.leave_room(driver_email)
        print(f'Driver {driver_email} disconnected')

@socket_io.on('route-changed')
def handle_route_changed(data):
    driver_id = data.get("driver_id") 
    driver_email = get_driver_email_by_id(driver_id)
    if driver_email:
        socket_io.emit('custom-notification', {"message": data["route"]}, room=driver_email)
        print(f'Route changed notification sent to Driver {driver_email}')