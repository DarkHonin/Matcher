const userInfoSocket = io.connect('http://' + document.domain + ':' + location.port + "/user_socket_transactions");

function userServerConnected(){
	displayMessage("User sockets connected")
}

function comeOnline(uname){
	item = document.querySelector("[data-uname='"+uname.user+"']")
	console.log(item)
	if(item)
		item.classList.add("online")
}

function goneOffline(uname){
	item = document.querySelector("[data-uname='"+uname.user+"']")
	console.log(item)
	if(item)
		item.classList.remove("online")
}

function checkStatus(){
	userInfoSocket.emit("accountStatus")
}

function accountStatus(message){
	translate(message)
}

function updateNotify(data){
	console.log(data)
}

userInfoSocket.on("connect", userServerConnected)
userInfoSocket.on("accountStatus", accountStatus)
userInfoSocket.on("now_online", comeOnline)
userInfoSocket.on("now_offline", goneOffline)
userInfoSocket.on("notify", updateNotify)

setInterval(checkStatus, 60000)
checkStatus()