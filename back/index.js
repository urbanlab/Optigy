var server = require('http').createServer();
var socket = require('socket.io')(server);
var PythonShell = require('python-shell');
var pyshell = new PythonShell('../demo/main.py', {mode:'json'});
var fs = require("fs");

var consommations;

pyshell.on('message', function(message) {
	consommations = JSON.parse(message);
	socket.emit('resultats', consommation);
});

pyshell.end((erreur) => {if(erreur) throw erreur});



socket.on('connection', (client) => {
    let contents = fs.readFileSync("../data/serie.json");
    let jsoncontent = JSON.parse(contents);
    socket.emit("resulats", jsoncontent);
});

server.listen(3000);