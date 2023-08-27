# from website import make_app
from flask_socketio import SocketIO, join_room, leave_room, send
from flask import Flask, session
#import geventwebsocket.gunicorn.workers

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
    print("Message sent")  # Emit the message

@socket_io.on('notifications')
def handle_notification():
    room = "ica@gmail.com"
    message = "salut"
    socket_io.emit('notifications', {'message': message}, room=room)
    print(f'Sent notification to room {room}: {message}')
    socket_io.emit('notification-sent')

@socket_io.on('subscribe')
def handle_subscribe(data):
    room = 'ica@gmail.com'
    join_room(room)
    print(f'Client joined room: {room}')

@socket_io.on('unsubscribe')
def handle_unsubscribe(data):
    room = data['room']
    leave_room(room)
    print(f'Client left room: {room}')

from website import callback

if __name__ == '__main__':
    app.run()
    gevent_worker = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
    socket_io.run(app, port=50000)#, worker=gevent_worker)