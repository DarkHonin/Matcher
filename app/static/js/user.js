
const page_display = document.querySelector("#pageDisplay")

var socket = io.connect('http://' + document.domain + ':' + location.port+"/home");
socket.on('connect', function() {
	socket.emit("getPage", {token: SessionToken, page:"home"});
});

socket.on('show_page', function(data){
	page_display.innerHTML = data
	bindEvents()
})

socket.on("error", function(error){
	var elm = document.getElementById("message")
	elm.classList.remove("ok")
	elm.classList.add("warning")
	elm.innerHTML = error
})

function goToPage(event){
	event.preventDefault()
	page = event.target.getAttribute("page")
	console.log("Fetching page: "+page)
	socket.emit("getPage", {token: SessionToken, page:page});
}

function saveInfo(event){
	var data = {}
	document.querySelectorAll("._field_input").forEach(f=>{
		name = f.getAttribute("name")
		value = f.value
		data[name] = value
	})
	console.log(data)
	socket.emit("saveData", {token: SessionToken, data : data});
}