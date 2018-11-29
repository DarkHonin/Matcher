
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
	grecaptcha.ready(function() {
		grecaptcha.execute('6LfKuH0UAAAAAJpKGjX7auo3dbt29wtjm4_FtATC')
			.then(function(token) {
				var fd = new FormData(event.target)
				var o = {}
				fd.forEach((v, k) => { o[k] = v})
				o["g-recaptcha-response"] = token
				transmit(event.target.action, o).then(d => translate(d), method="post")
			});
	});
}

function displayMessage(message, state=true){
	var elm = document.getElementById("message")
	if(state) 	elm.style.backgroundColor = "RGBA(90, 255, 90, 0.6)"
	else		elm.style.backgroundColor = "RGBA(255, 90, 90, 0.6)"
	elm.innerHTML = message
	setTimeout(() => {elm.style.opacity = 0}, 5000)
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

