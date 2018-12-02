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
				event.target.style.opacity = 0
			});
	});
}

function addImage(event){
	file = event.target.files[0]
	if(file.type != "image/jpeg" && file.type != "image/jpg")
		return alert("The image must be of type jpeg/jpg")
	if(file.size > 2097152)
		return alert("The image must be smaller than 2MB")
	reader = new FileReader()
	reader.onloadend = function(){
		grecaptcha.ready(function() {
			grecaptcha.execute('6LfKuH0UAAAAAJpKGjX7auo3dbt29wtjm4_FtATC')
				.then(function(token) {
					var o = {data : reader.result}
					o["g-recaptcha-response"] = token
					transmit("/settings", o, method="insert").then(d => translate(d))
				});
		});
	}

	reader.readAsDataURL(file)
}

const preview = document.querySelector(".preview")

function insertImage(imageUrl){
	img = new Image()
	img.src = imageUrl
	img.classList.add("usr_img")
	inserter = document.getElementById("imageinput")
	img.addEventListener('click', previewImage)
	document.querySelectorAll(".carosel>.selected").forEach(f => {f.classList.remove("selected")})
	inserter.parentNode.insertBefore(img, inserter)
	img.click()
}

function previewImage(event){
	preview.src = event.target.src
	preview.classList.remove("empty")
}

function tagTyped(event){
	if(event.key != "," || event.target.value.length < 3)
		return
	var elm = document.createElement("span")
	id = event.target.getAttribute("data-input")
	elm.innerHTML = event.target.value.replace(",", "")
	elm.setAttribute("data-input", id)
	elm.addEventListener("click", destroyTag)
	input = document.getElementById(id)
	event.target.value = ""
	var arr = JSON.parse(input.value.replace(/'/g, '"'))
	if(arr.indexOf(elm.innerHTML) > 0)
		return
	arr.push(elm.innerHTML)
	input.value = JSON.stringify(arr)
	input.dispatchEvent(new Event('change'))
	event.target.parentNode.querySelector(".items").appendChild(elm)
}

function destroyTag(event){
	input = document.getElementById(event.target.getAttribute("data-input"))
	var arr = JSON.parse(input.value.replace(/'/g, '"'))
	var str = event.target.innerHTML
	var index = arr.indexOf(str)
	arr.splice(index, 1)
	input.value = JSON.stringify(arr)
	input.dispatchEvent(new Event('change'))
	event.target.remove()
}