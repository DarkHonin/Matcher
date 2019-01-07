const socket = io.connect('http://' + document.domain + ':' + location.port + "/messages");

socket.on('connect', function() {
	socket.emit('init', {token : __USERTOKEN});
});

socket.on("general_socket_handle", translate)

socket.on("start_requests", function(){
	var tm = setInterval(function(){
		socket.emit("getMessages")
	}, 1000)

	socket.on("disconnect", () => {clearInterval(tm)})
})