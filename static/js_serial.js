const canal_entrada = "canal_servidor_cliente";
const canal_salida = "canal_cliente_servidor";


class JsSerial {
    constructor() {
        this.socket = io('ws://localhost:7345');
        this.socket.on('connect', function() { console.log("websocket conectado") });
        this.socket.on('event', function(data) { console.log(data) });
        this.socket.on('disconnect', function() { console.log("websocket desconectado") });
    }

    open() {
        console.log("not implemented yet");
    }

    on(command, cb) {
        switch (command) {
            case 'data':
                this.socket.on(canal_entrada, cb);
                break;
        }
    }

    write(msg) {
        this.socket.emit(canal_salida, msg);
    }
}