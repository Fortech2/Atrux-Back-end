from website import make_app
from flask_socketio import SocketIO
import time

app = make_app()

socket_io = SocketIO(app, cors_allowed_origins="*")
@socket_io.on('connect')
def handle_connect():
    print('new connection')

@socket_io.on('to-server')
def handle_to_server(arg):
    print(f'new to-server event: {arg}')
    socket_io.emit('from-server', str(time()))

if __name__ == '__main__':
    app.run(debug=True)
    socket_io = SocketIO(app, cors_allowed_origins="*")
    socket_io.run(app, port=50000)