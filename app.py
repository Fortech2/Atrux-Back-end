from website import make_app
from socketio_manager import socket_io

app = make_app()
socket_io.init_app(app)

if __name__ == '__main__':
    socket_io.run(app, host='0.0.0.0', port=5000, log_output=True, server="gevent")