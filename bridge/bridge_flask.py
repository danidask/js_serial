# from gevent import monkey
# monkey.patch_all()
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
# ,jsonify , abort, make_response
from flask_socketio import SocketIO, send, emit
from bridge_serial import BridgeSerial
import threading
from time import sleep

canal_salida = "canal_servidor_cliente"
canal_entrada = "canal_cliente_servidor"

app = Flask(__name__, static_url_path="/static", template_folder="templates")
app.secret_key = "_5#y2LF4Q8zdsfasdf342xec]"
socketio = SocketIO(app, cors_allowed_origins="*", cors_credentials=False)


def bridge_serial_callback(msg):
    with app.test_request_context('/'):
       socketio.emit(canal_salida, msg)

def prueba_sock():
    global app
    while 1:
        print("enviando")
        with app.test_request_context('/'):
            socketio.emit(canal_salida, "12564552")
        sleep(5)


@app.route('/', methods=['GET', ])
def vista_home():

    context = {}
    return render_template('index.html', **context)

@app.route('/send', methods=['GET', ])
def vista_send():
    msg = "test test ========================="
    with app.test_request_context('/'):
        socketio.emit(canal_salida, msg)
    return "ok"


@socketio.on(canal_entrada)
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    bridge_serial = BridgeSerial()
    bridge_serial.callback(bridge_serial_callback)
    bridge_serial.connect()
    # thread1 = threading.Thread(target=prueba_sock)
    # thread1.start()
    try:
        socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    except (KeyboardInterrupt, SystemExit):
        pass
    bridge_serial.stop()
