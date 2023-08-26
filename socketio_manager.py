from flask_socketio import SocketIO
from website.models import Driver
from flask_socketio import join_room, leave_room



socket_io = SocketIO(cors_allowed_origins="*", async_mode="gevent")

def get_driver_email_by_id(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        return driver.email
    return None

@socket_io.on('connecting')
def handle_connect(driver_email):
    join_room(driver_email)
    print(f'Driver {driver_email} connected')

@socket_io.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socket_io.on('route-changed')
def handle_route_changed(data):
    driver_email = data.get("driver_email")
    socket_io.emit('custom-notification', {"message": data["route"]}, room=driver_email)
    print(f'Route changed notification sent to Driver {driver_email}')