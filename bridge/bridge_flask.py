
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
# ,jsonify , abort, make_response
from flask_socketio import SocketIO, send, emit

canal_salida = "canal_servidor_cliente"
canal_entrada = "canal_cliente_servidor"

app = Flask(__name__, static_url_path="/static", template_folder="templates")
app.secret_key = "_5#y2LF4Q8zdsfasdf342xec]"
socketio = SocketIO(app, cors_allowed_origins="*", cors_credentials=False)


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
    try:
        socketio.run(app, host="0.0.0.0", port=5000, debug=True)
        # app.run(host="0.0.0.0", port=settings.WEB_PORT, debug=settings.WEB_DEBUG)
    except (KeyboardInterrupt, SystemExit):
        pass
