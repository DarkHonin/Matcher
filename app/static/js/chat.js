const chat = io.connect('http://' + document.domain + ':' + location.port + "/chat");

function selectChat(item, uid){
	console.log(item)
	chat.emit("get_messages", {id : uid})
}