
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

function editField(event){
	event.preventDefault()
	var field = event.target.parentNode.parentNode.querySelector(".data")
	var name = field.getAttribute("name")
	if(! event.target.state || event.target.state == "Waiting"){
		transmit("/userSettings/"+name, {}, "GET").then(t => {
			if(t.status == "NOJOY")
				return displayMessage("Failed to prepare state", false)
			framgent = document.createRange().createContextualFragment(t.data)
			field.parentNode.appendChild(framgent)
			field.remove()
			event.target.innerHTML = "Save"
			event.target.state = "Editing"
		})
	}else{
		transmit("/userSettings/"+name, {token: SessionToken, value:field.value}).then(t => {
			if(t.status == "NOJOY")
				return displayMessage(t.message, false)
			if(field.getAttribute("type") == "password")
				framgent = document.createRange().createContextualFragment("<span class='data' name='"+name+"'>Super secret</span>")
			else
				framgent = document.createRange().createContextualFragment("<span class='data' name='"+name+"'>"+field.value+"</span>")
			field.parentNode.appendChild(framgent)
			field.remove()
			event.target.innerHTML = "Edit"
			event.target.state = "Waiting"
		})
	}
}