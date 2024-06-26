# from website import make_app
from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room

# app = make_app()
app = Flask(__name__)
rooms = {}


socket_io = SocketIO(app, cors_allowed_origins="*") #, async_mode='gevent')

@socket_io.on('connect')
def handle_connect():
    print('new connection')
    socket_io.emit('from-server', 'hello from backend')

@socket_io.on('disconnect')
def handle_disconnect():
    print('disconnected')

@socket_io.on('to-server')
def handle_to_server(arg):
    print(f'new to-server event: {arg}')
    socket_io.emit('to-server', f'{arg}')
    print("Message sent")

@socket_io.on('notifications')
def handle_notification(driver_email):
    room = driver_email 
    message = "New route from your dispatcher"
    socket_io.emit('notifications', {'message': message}, room=room)
    print(f'Sent notification to driver {room}: {message}')
    socket_io.emit('notification-sent')

@socket_io.on('handle-images')
def handle_images(driver_email):
    room = driver_email 
    message = "Motion Detected"
    socket_io.emit('handle-images', {'message': message}, room=room)
    print(f'Sent image notification to driver {room}: {message}')
    socket_io.emit('image-notification-sent')

@socket_io.on('subscribe')
def handle_subscribe(data):
    driver_email = data['driver_email']  
    room = driver_email
    join_room(room)
    print(f'Client joined room: {room}')

@socket_io.on('unsubscribe')
def handle_unsubscribe(data):
    room = data['room']
    leave_room(room)
    print(f'Client left room: {room}')

from website import callback

if __name__ == '__app__':
    app.run()
    gevent_worker = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
    socket_io.run(app, port=50000)#, worker=gevent_worker)