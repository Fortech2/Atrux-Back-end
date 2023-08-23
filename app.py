from website import make_app
from flask_socketio import SocketIO
#import geventwebsocket.gunicorn.workers

app = make_app()

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
    socket_io.emit('from-server', 'hello from backend daisojfo iajoifjoiasfij')  # Emit the message

if __name__ == '__main__':
    gevent_worker = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
    socket_io.run(app, port=50000)#, worker=gevent_worker)