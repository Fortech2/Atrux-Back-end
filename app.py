from website import make_app
from socketio_manager import socket_io
import geventwebsocket.gunicorn.workers

app = make_app()
socket_io.init_app(app)
if __name__ == '__main__':
    gevent_worker = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
    socket_io.run(app, port=50000, worker=gevent_worker)