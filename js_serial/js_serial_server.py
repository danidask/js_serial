# from gevent import monkey
# monkey.patch_all()
import eventlet
eventlet.monkey_patch()

import socketio
import argparse
from .js_serial_serial import BridgeSerial

canal_salida = "canal_servidor_cliente"
canal_entrada = "canal_cliente_servidor"
clients = set()

sio = socketio.Server(cors_allowed_origins='*')
# https://python-socketio.readthedocs.io/en/latest/server.html
static_files = {
    '/': 'templates/index.html',
    '/sketch.js': 'static/sketch.js',
    '/js_serial.js': 'static/js_serial.js',
}
app = socketio.WSGIApp(sio, static_files=static_files)
bridge_serial = BridgeSerial()


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
    # sio.emit(canal_salida, {'response': 'my response'})
    bridge_serial.write(data.encode())


def bridge_serial_callback(msg):
    # print(msg)
    # https://python-socketio.readthedocs.io/en/latest/server.html#emitting-events
    sio.emit(canal_salida, msg)
    # temp_clients = clients # RuntimeError: Set changed size during iteration
    # for client in temp_clients:
    #     sio.emit('status', {'msg': 'name entered the room.'}, room=client)
    # sio.send(msg, to=client, namespace=None, callback=None)
    # sio.emit(canal_salida, {'response': 'my response'})


def main():
    parser = argparse.ArgumentParser(description='Launch server.')
    parser.add_argument('-b', '--baudrate', default='57600', type=int, help='baudrate (default: 57600)')
    parser.add_argument('-p', '--port',  default='', help='serial port (default: autodetect)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Prints messages')
    args = parser.parse_args()

    port = args.port if args.port else None
    bridge_serial.set_callback(bridge_serial_callback)
    bridge_serial.connect(port=port, baudrate=args.baudrate, verbose=args.verbose)
    try:
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 7345)), app)
    except (KeyboardInterrupt, SystemExit):
        pass
    bridge_serial.stop()


if __name__ == '__main__':
    main()
