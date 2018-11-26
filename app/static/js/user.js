function edit_profile(event){

}

function update_telemetry(){
	console.log("Starting state update")
	transmit("/home", {}, "INFO").then( data => {translate(data)})
	console.log("Update ended")
}

var socket = new WebSocket("ws://localhost:5000/home");
socket.onopen = function(){
	console.log("Connection open")
	socket.send(JSON.stringify({"connect":"Special token"}));
}
socket.onmessage = function(data){
	console.log(data.data)
}