const notifications = io.connect('http://' + document.domain + ':' + location.port + "/notfications");


function comeOnline({id}){
	item = document.querySelectorAll("[uid='"+id+"']").forEach(f => {f.classList.add("online"); console.log(f.getAttribute("data-uname"), "is now online")})
	
}

function goneOffline({id}){
	item = document.querySelectorAll("[uid='"+id+"']").forEach(f => {f.classList.remove("online");})
}

function pushNotification(message){
	displayMessage({message : message})
	notifications.emit("get_notif_count")
}

function notif_count({messages, alerts}){
	if (alerts == 0)
		document.querySelector("#notifications").setAttribute("data-counter", "")
	else
		document.querySelector("#notifications").setAttribute("data-counter", alerts)
	if (messages == 0)
		document.querySelector("#messages").setAttribute("data-counter", "")
	else
		document.querySelector("#messages").setAttribute("data-counter", messages)
}

window.addEventListener("close", event => {notifications.disconnect()})
window.addEventListener("beforeunload", event => {notifications.disconnect()})

notifications.on("notification", pushNotification)
notifications.on("online", comeOnline)
notifications.on("offline", goneOffline)
notifications.on("notif_count", notif_count)

function check_online(){
	document.querySelectorAll("[uid]").forEach(f => {
		notifications.emit("isOnline", {id : f.getAttribute("uid")})
	})
}