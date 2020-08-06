let socket;
const canal_entrada = "canal_servidor_cliente";
const canal_salida = "canal_cliente_servidor";


function setup() {
    noCanvas();
    noLoop();

    // socket = io('http://' + rhost);
    socket = io('http://192.168.1.130:5000');
    // console.log(socket);
    // socket.io.set('origins', '*');
    socket.on('connect', function() { console.log("websocket conectado") });
    socket.on('event', function(data) { console.log(data) });
    socket.on('disconnect', function() { console.log("websocket desconectado") });

    socket.on(canal_entrada, socket_cb); // canal viene en la plantilla

    createButton("ejemplo").mousePressed(ejemplo_boton);
    console.log("inicio");
}

function ejemplo_boton() {
    msg = "prueba"
    console.log("enviado: '" + msg + "' por canal " + canal_salida);
    socket.emit(canal_salida, msg);
}

function socket_cb(data) {
    console.log("================");
    console.log(data);
    // let jdata = JSON.parse(data);
    //if (typeof(jdata.presion) != "undefined"){

}