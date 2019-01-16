const notifications = io.connect('http://' + document.domain + ':' + location.port + "/notfications", {'multiplex': false});


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

function notif_count(alerts){
	if (alerts == 0)
		document.querySelector("#notifications").setAttribute("data-counter", "")
	else
		document.querySelector("#notifications").setAttribute("data-counter", alerts)
	
}

function msg_count(msgs){
	if (msgs == 0)
		document.querySelector("#messages").setAttribute("data-counter", "")
	else
		document.querySelector("#messages").setAttribute("data-counter", msgs)
}

function chat_count({count, chat_id}){
	elm = document.querySelector("[chat_id='"+chat_id+"']")
	if (count == 0)
		elm.setAttribute("data-counter", "")
	else
		elm.setAttribute("data-counter", count)
}

window.addEventListener("close", event => {notifications.disconnect()})
window.addEventListener("beforeunload", event => {notifications.disconnect()})

notifications.on("notification", pushNotification)
notifications.on("online", comeOnline)
notifications.on("offline", goneOffline)
notifications.on("alert_count", notif_count)
notifications.on("message_count", msg_count)
notifications.on("chat_count", chat_count)

function check_online(){
	document.querySelectorAll("[uid]").forEach(f => {
		notifications.emit("isOnline", {id : f.getAttribute("uid")})
	})
}