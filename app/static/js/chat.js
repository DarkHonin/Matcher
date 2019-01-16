const chat = io.connect('http://' + document.domain + ':' + location.port + "/chat", {'multiplex': false});

function getActiveID(){
	return document.querySelector("[chat_id].active").getAttribute("chat_id")
}

function selectChat(item){
	uid = item.getAttribute("chat_id")
	el = document.querySelector(".chat_space>.messsages")
	el.classList.add("empty")
	chat.emit("get_messages", {id : uid})
}

function setChatActive(id){
	document.querySelectorAll("[chat_id].active").forEach(f => {f.classList.remove("active")})
	document.querySelector("[chat_id='"+id+"']").classList.add("active")
}

function sendMessage(event){
	event.preventDefault()
	msg = event.target.parentNode.querySelector("input").value
	event.target.parentNode.querySelector("input").value = ""
	id = document.querySelector("[chat_id].active").getAttribute("chat_id")
	chat.emit("message_send", msg, id)
}


function displayChatMessages(messages){
	hist = document.querySelector(".chat_space>.messsages>.history")
	hist.innerHTML = ""
	messages.forEach(e=>{
		hist.appendChild(createMessageElement(e))	
	})
	hist.scrollTop = hist.scrollHeight
}

function createMessageElement(message){
	sp = document.createElement("span")
		if (message.user == user_id) sp.classList.add("current_user")
		sp.innerHTML = message.message
		sp.setAttribute("data-time", message.time)
		return sp;
}

chat.on("show_chat", function({messages, chat_id}){
	setChatActive(chat_id)
	document.querySelector(".chat_space>.messsages").classList.remove("empty")
	displayChatMessages(messages)
	chat.emit("read", chat_id=getActiveID())
})

chat.on("chat_pending", function({chat_id}){
	setChatActive(chat_id)
	el = document.querySelector(".chat_space>.no_messages")
	el.innerHTML = "UQ"
	el.setAttribute("data-text", "This chat is still pending")
})

chat.on("message_get", function({message}){
	hist = document.querySelector(".chat_space>.messsages>.history")
	hist.appendChild(createMessageElement(message))
	hist.scrollTop = hist.scrollHeight
	chat.emit("read", chat_id=getActiveID())
})

chat.on("unread_chats", function(unread){
	unread.forEach(q => {
		document.querySelector("[chat_id='"+q.chat_id+"']").setAttribute("data-counter", q.count)
	})
	console.log(unread)
})