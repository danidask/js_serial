import eventlet
import socketio
from bridge_serial import BridgeSerial

canal_salida = "canal_servidor_cliente"
canal_entrada = "canal_cliente_servidor"
clients = set()

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

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
    sio.emit(canal_salida, {'data': 'foobar'})
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
