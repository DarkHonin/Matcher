const socket = io.connect('http://' + document.domain + ':' + location.port + "/user_transmissions");

socket.on('connect', function() {
    
});

function checkMessages(){
	socket.emit("messages")
}

setInterval(checkMessages, 5000)

