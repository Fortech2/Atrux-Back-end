from flask_socketio import SocketIO
from website.models import Driver
from flask_socketio import join_room, leave_room
from website.auth import get_user_data


socket_io = SocketIO(cors_allowed_origins="*", manage_session=True)

def get_driver_email_by_id(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        return driver.email
    return None

# @socket_io.on('connect')
# def handle_connect():
#     user_data_response = get_user_data()
#     if user_data_response.status_code == 200:
#         user_data = user_data_response.json()
#         user_id = user_data["id"]
#         driver_email = get_driver_email_by_id(user_id)
#         if driver_email:
#             join_room(driver_email)
#             print(f'Driver {driver_email} connected')
#         else:
#             # Handle the case where user is not authenticated properly
#             pass
#     else:
#         # Handle the case where user data retrieval failed
#         pass


@socket_io.on('connect')
def handle_connect():
    print('new connection')
    socket_io.emit('from-server', 'hello from backend')
@socket_io.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socket_io.on('route-changed')
def handle_route_changed(data):
    driver_email = data.get("driver_email")
    route = data.get("route")
    
    if driver_email and route:
        socket_io.emit('custom-notification', {"message": route}, room=driver_email)
        print(f'Route changed notification sent to Driver {driver_email}')
    else:
        print('Missing or incomplete data in route-changed event')