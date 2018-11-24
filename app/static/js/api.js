
const path = window.location.pathname;

function transmit(url, data, method="post"){
	return fetch(url, { 
			method: method, 
			mode: "same-origin",
			cache: "no-cache",
			credentials: "same-origin",
			headers: {
				"Content-Type": "application/json; charset=utf-8",
			},
			redirect: "follow",
			referrer: "no-referrer",
			body: JSON.stringify(data),
		}).then(responce => responce.json());
}

function formSubmit(event){
	event.preventDefault()
	var fd = new FormData(event.target)
	var o = {}
	fd.forEach((v, k) => { o[k] = v})
	transmit(this.action, o).then(d => translate(d))
}

function display(message, state=true){
	var elm = document.getElementById("message")
	elm.classList.remove("ok")
	elm.classList.remove("error")
	if(state) 	elm.classList.add("ok")
	else		elm.classList.remove("error")
	elm.innerHTML = message
}

function field_error(field){
	document.querySelector("[name='"+field.item+"']").setCustomValidity(item.message);
}

function redirect(message){
	window.location.pathname = message
}

function translate(json){
	if(json.status != "JOY")
		return display(json.message, false)

	if(window[json.action])
		window[json.action](json.message)
}

document.querySelectorAll("[event]").forEach(f => {
	var j = JSON.parse(f.getAttribute("event"))
	for(var i in j){
		console.log("Binding: "+i+" to "+j[i])
		f.addEventListener(i, window[j[i]])
	}
})
