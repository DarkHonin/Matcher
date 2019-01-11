//const userInfoSocket = io.connect('http://' + document.domain + ':' + location.port + "/messages");

function comeOnline(uname){
	console.log(uname)
	item = document.querySelectorAll("[data-uname='"+uname.user+"']").forEach(f => {f.classList.add("online"); console.log(f)})
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


function APIButtonChange(mess){
	console.log(mess)
	item = document.querySelector("#"+mess.id)
	item.innerHTML = mess.innerHTML
}

function general(item){
	translate(item)
}

userInfoSocket.on("accountStatus", accountStatus)
userInfoSocket.on("now_online", comeOnline)
userInfoSocket.on("now_offline", goneOffline)
userInfoSocket.on("notify", updateNotify)
userInfoSocket.on("general", general)