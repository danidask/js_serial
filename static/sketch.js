let serial;
let output_div;


function setup() {
    noCanvas();
    noLoop();

    serial = new JsSerial();
    serial.open();
    serial.on('data', gotData);

    output_div = createDiv("Waiting...");
    createButton("Send").mousePressed(buttonExample);
}

function buttonExample() {
    msg = "test message"
    console.log("sent: '" + msg);
    serial.write(msg);
}

function gotData(data) {
    output_div.html(data);
    // let jdata = JSON.parse(data);
    //if (typeof(jdata.value) != "undefined"){ ... }
}