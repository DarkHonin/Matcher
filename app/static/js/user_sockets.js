const notifications = io.connect('http://' + document.domain + ':' + location.port + "/notfications");


function comeOnline({id}){
	item = document.querySelectorAll("[uid='"+id+"']").forEach(f => {f.classList.add("online"); console.log(f.getAttribute("data-uname"), "is now online")})
}

function goneOffline({id}){
	item = document.querySelectorAll("[uid='"+id+"']").forEach(f => {f.classList.remove("online");})
}

function checkStatus(){
	notifications.emit("accountStatus")
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

notifications.on("accountStatus", accountStatus)
notifications.on("online", comeOnline)
notifications.on("offline", goneOffline)
notifications.on("notify", updateNotify)
notifications.on("general", general)
notifications.on("connect", auth)

function check_online(){
	document.querySelectorAll("[uid]").forEach(f => {
		notifications.emit("isOnline", {id : f.getAttribute("uid")})
	})
}