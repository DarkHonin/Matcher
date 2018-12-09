const socket = io.connect('http://' + document.domain + ':' + location.port + "/user_socket_transactions");

function userServerConnected(){
	displayMessage("User sockets connected")
}



socket.on("connect", userServerConnected)
