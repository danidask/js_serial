let socket;
const canal_entrada = "canal_servidor_cliente";
const canal_salida = "canal_cliente_servidor";

let output_div;

function setup() {
    noCanvas();
    noLoop();

    socket = io('ws://localhost:7345');
    socket.on('connect', function() { console.log("websocket conectado") });
    socket.on('event', function(data) { console.log(data) });
    socket.on('disconnect', function() { console.log("websocket desconectado") });
    socket.on(canal_entrada, socket_cb);

    output_div = createDiv("Waiting...");
    createButton("Send").mousePressed(ejemplo_boton);
}

function ejemplo_boton() {
    msg = "test message"
    console.log("sent: '" + msg + "' channel " + canal_salida);
    socket.emit(canal_salida, msg);
}

function socket_cb(data) {
    output_div.html(data);
    // let jdata = JSON.parse(data);
    //if (typeof(jdata.value) != "undefined"){
}
