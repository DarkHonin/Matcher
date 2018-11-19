const state = document.querySelector("#page_state").value
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

function load(key, data){
	var components = document.querySelectorAll(key)
	transmit(data.url, data.params).then(resp => {
		if(resp.status != "JOY")
			return alert("There was a problem fetching the page");
		components.forEach(c => {
			c.innerHTML = resp.payload
		})
	})
}

function translate(json){
	if(json.status != "JOY")
		return alert("There was a problem fetching the page");

	var payload = json.payload

	for(var i in payload){
		if (payload.hasOwnProperty(i)){
			var q = payload[i];
			if(window[q.action])
				window[q.action](i, q)
			}
	}
}

transmit(path, {"id" : state}).then(resp => {translate(resp)}).catch(error => console.error(error));
