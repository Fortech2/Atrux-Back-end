from website import make_app
from flask_socketio import SocketIO
#import geventwebsocket.gunicorn.workers
from website.models import Driver
app = make_app()
connected_drivers = set() 
socket_io = SocketIO(app, cors_allowed_origins="*") #, async_mode='gevent')
def get_driver_email_by_id(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        return driver.email
    return None

@socket_io.on('connect')
def handle_connect(driver_id):
    driver_email = get_driver_email_by_id(driver_id)
    if driver_email:
        connected_drivers.add(driver_id)
        socket_io.join_room(driver_email)
        print(f'Driver {driver_email} connected')

@socket_io.on('disconnect')
def handle_disconnect(driver_id):
    driver_email = get_driver_email_by_id(driver_id)
    if driver_email in connected_drivers:
        connected_drivers.remove(driver_id)
        socket_io.leave_room(driver_email)
        print(f'Driver {driver_email} disconnected')

if __name__ == '__main__':
    gevent_worker = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
    socket_io.run(app, port=50000)#, worker=gevent_worker)