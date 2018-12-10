const userInfoSocket = io.connect('http://' + document.domain + ':' + location.port + "/user_socket_transactions");

function userServerConnected(){
	displayMessage("User sockets connected")
}


function checkStatus(){
	userInfoSocket.emit("accountStatus")
}

function accountStatus(message){
	translate(message)
}

userInfoSocket.on("connect", userServerConnected)
userInfoSocket.on("accountStatus", accountStatus)

setInterval(checkStatus, 60000)
checkStatus()