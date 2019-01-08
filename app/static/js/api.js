
const path = window.location.pathname;

function transmit(url, data, method="post"){
	console.log("Transit - "+url+" - "+method)
	head = { 
		method: method, 
		mode: "same-origin",
		cache: "no-cache",
		credentials: "include",
		headers: {
			"Content-Type": "application/json; charset=utf-8",
		},
		redirect: "follow",
		referrer: "no-referrer",
	}
	if(method != "GET")
		head["body"] = JSON.stringify(data)
	document.querySelectorAll("[data-field]").forEach(f => f.removeAttribute("data-error"))
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

var messageHideHook = null

function displayMessage({message, state=true, persist=false}){
	var elm = document.getElementById("message")
	console.log("state is", state)
	if(state) 	elm.style.backgroundColor = "RGBA(90, 255, 90, 0.6)"
	else		elm.style.backgroundColor = "RGBA(255, 90, 90, 0.6)"
	elm.innerHTML = message
	if(messageHideHook)
		clearTimeout(messageHideHook)
	if(!persist)
		messageHideHook = setTimeout(() => {
			elm.innerHTML = ""
			messageHideHook = null
		}, 5000)
}

function redirect({location}){
	setTimeout(function(){
		window.location.pathname = location
	}, 5200)
}

function translate(json){
	if(!json.handle)
		displayMessage("Impropper server responce")
	console.log("Resloveing handle:", json.handle, " >> ", window[json.handle] != undefined)
	if(window[json.handle])
		window[json.handle](json.data)
}

function carosel_shift(event){
	if(! (elm = event.target.nextElementSibling))
		if (!(elm = event.target.parentNode.firstElementChild))
			return
	event.target.classList.remove("show")
	elm.classList.add("show")
}

function APIFieldErrorMessage(data){
	console.log("Handeling field error responce")
	for(i in data){
		var elm = document.querySelector("[data-field="+i+"]")
		if(elm)
			elm.setAttribute("data-error", data[i])
	}
}

function APIException(data){
	displayMessage(data, false)
}

function update({insert, fn, data}){
	inst = document.querySelector(insert)
	if (!inst)
		return console.log("could not update", insert, "Element not found")
	if (!window[fn])
		return console.log("could not update", insert, "Function not found : ", fn)
	inst.appendChild(fn(data))
}

function APISuccessMessage(data){
	console.log(data)
	for(e in data){
		console.log(e, data[e])
		if(window[e])
			window[e](data[e])
	}
}
