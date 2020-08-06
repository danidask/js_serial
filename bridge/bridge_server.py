# from gevent import monkey
# monkey.patch_all()
import eventlet
eventlet.monkey_patch()

import socketio
from bridge_serial import BridgeSerial

canal_salida = "canal_servidor_cliente"
canal_entrada = "canal_cliente_servidor"
clients = set()

sio = socketio.Server(cors_allowed_origins='*')
# https://python-socketio.readthedocs.io/en/latest/server.html
static_files = {
    '/': 'templates/index.html',
    '/static/sketch.js': 'static/sketch.js',
}
app = socketio.WSGIApp(sio, static_files=static_files)

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    clients.add(sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    clients.discard(sid)

@sio.on(canal_entrada)
def msg_canal_entrada(sid, data):
    print('message ', data)
    #sio.emit(canal_salida, {'response': 'my response'})

def bridge_serial_callback(msg):
    print("recibido por serie, se reenvia:")
    #print(msg)
#https://python-socketio.readthedocs.io/en/latest/server.html#emitting-events
    sio.emit(canal_salida, msg)
    #temp_clients = clients # RuntimeError: Set changed size during iteration
    #for client in temp_clients:
    #    sio.emit('status', {'msg': 'name entered the room.'}, room=client)
        #sio.send(msg, to=client, namespace=None, callback=None)
    #sio.emit(canal_salida, {'response': 'my response'})


if __name__ == '__main__':
    bridge_serial = BridgeSerial()
    bridge_serial.callback(bridge_serial_callback)
    bridge_serial.connect()
    try:
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
    except (KeyboardInterrupt, SystemExit):
        pass
    bridge_serial.stop()
