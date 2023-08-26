from website import make_app
from socketio_manager import socket_io
import geventwebsocket.gunicorn.workers

app = make_app()
socket_io.init_app(app)
if __name__ == '__main__':
    from gevent import pywsgi
    
    server = pywsgi.WSGIServer(("0.0.0.0", 50000), app, handler_class=geventwebsocket.gunicorn.workers.GeventWebSocketHandler)
    server.serve_forever()