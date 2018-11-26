
const page_display = document.querySelector("#pageDisplay")

var socket = io.connect('http://' + document.domain + ':' + location.port+"/home");
socket.on('connect', function() {
	socket.emit("getPage", {token: SessionToken, page:"home"});
});

socket.on('show_page', function(data){
	console.log(data)
	page_display.innerHTML = data
})

socket.on("error", function(error){
	var elm = document.getElementById("message")
	elm.classList.remove("ok")
	elm.classList.add("warning")
	elm.innerHTML = error
})