let server = require('http').createServer();
let socket = require('socket.io')(server);
let fs = require("fs");

server.listen(3000);

socket.on('connection', (client) => {
    client.on('disconnect', () => {
	console.log("disconnected");
    });
    let contents = fs.readFileSync("serie.json");
    let jsoncontent = JSON.parse(contents);
    console.log(jsoncontent);
    socket.emit("value", jsoncontent);
});
