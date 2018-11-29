function showSaveButton(event){
	event.target.parentNode.querySelector("button").style.opacity = 1
}

function saveField(event){
	field = event.target.parentNode.querySelector(".data")
	data = field.value
	name = field.getAttribute("name")
	item = event.target.getAttribute("data-type");
	id = event.target.getAttribute("data-id");
	grecaptcha.ready(function() {
		grecaptcha.execute('6LfKuH0UAAAAAJpKGjX7auo3dbt29wtjm4_FtATC')
			.then(function(token) {
				var o = {
							key : name,
							item : item,
							id : id
						}
				o[name] = data
				o["g-recaptcha-response"] = token
				transmit("/settings", o).then(d => translate(d), method="post")
			});
	});
}