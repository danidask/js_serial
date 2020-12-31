const input_channel = "ch_srv_clnt";
const output_channel = "ch_clnt_srv";

class JsSerial {
    constructor() {
        this.connected = false;
        this.connect_cb = null;
        this.disconnect_cb = null;        
        this.socket = io('ws://localhost:7345');
        this.socket.on('connect', () => { 
            console.log("websocket connected");
            this.connected = true;
            if (this.connect_cb)
                this.connect_cb()
         });
        this.socket.on('disconnect', () => { 
            console.log("websocket disconnected");
            this.connected = false;
            if (this.disconnect_cb)
                this.disconnect_cb()
        });
        this.socket.on('event', function(data) { console.log(data) });
    }

    open() {
        console.log("not implemented yet");
    }

    on(command, cb) {
        switch (command) {
            case 'data':
                this.socket.on(input_channel, cb);
                break;
            case 'connect':
                this.connect_cb = cb;
                break;
            case 'disconnect':
                this.disconnect_cb = cb;
                break;
            default:
                console.error(`JsSerial: ${command} not supported`);
                break;              
        }
    }

    write(msg) {
        if (typeof msg === 'object')
            msg = JSON.stringify(msg)
        else if (typeof msg != 'string'){
            msg = String(msg)
        }
        this.socket.emit(output_channel, msg);
    }

    isConnected(){
        return this.connected;
    }
}
