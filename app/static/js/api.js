
const path = window.location.pathname;

function transmit(url, data, method="post"){
	console.log("Transit - "+url+" - "+method)
	head = { 
		method: method, 
		mode: "same-origin",
		cache: "no-cache",
		credentials: "same-origin",
		headers: {
			"Content-Type": "application/json; charset=utf-8",
		},
		redirect: "follow",
		referrer: "no-referrer",
	}
	if(method != "GET")
		head["body"] = JSON.stringify(data)
	return fetch(url, head).then(responce => responce.json());
}

function bindEvents(){
	document.querySelectorAll("[event]").forEach(f => {
		var j = JSON.parse(f.getAttribute("event"))
		if(!f["eventsLoaded"]){
			f.eventsLoaded = true
			for(var i in j){
				console.log("Binding: "+i+" to "+j[i]+f)
				f.addEventListener(i, window[j[i]])
			}
		}
	})
}

function formSubmit(event){
	event.preventDefault()
	var fd = new FormData(event.target)
	var o = {}
	fd.forEach((v, k) => { o[k] = v})
	transmit(this.action, o).then(d => translate(d), method="post")
}

function displayMessage(message, state=true){
	var elm = document.getElementById("message")
	elm.classList.remove("ok")
	elm.classList.remove("warning")
	if(state) 	elm.classList.add("ok")
	else		elm.classList.add("warning")
	elm.innerHTML = message
}

function field_error(field){
	document.querySelector("[name='"+field.item+"']").setCustomValidity(item.message);
}

function redirect(message){
	setTimeout(function(){
		window.location.pathname = message
	}, 1000)
}

function translate(json){
	for(var a in json.actions){
		if(window[a])
			window[a](json.actions[a], json.state == "JOY")
	}
}


