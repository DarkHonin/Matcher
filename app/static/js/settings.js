function showSaveButton(event){
	event.target.parentNode.querySelector(".saveBTN").classList.add("show")
}

function saveField(event){
	field = event.target.nextSibling.nextSibling
	data = field.value
	name = field.getAttribute("name")
	grecaptcha.ready(function() {
		grecaptcha.execute('6LfKuH0UAAAAAJpKGjX7auo3dbt29wtjm4_FtATC')
			.then(function(token) {
				var o = {}
				o[name] = data
				o["g-recaptcha-response"] = token
				transmit(document.location, o).then(d => translate(d), method="post")
				event.target.classList.remove("show")
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
					var o = {image : reader.result}
					o["g-recaptcha-response"] = token
					transmit(window.location, o).then(d => translate(d))
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
	preview.setAttribute("image_id", event.target.getAttribute("image_id"))
	preview.classList.remove("empty")
}

var tagList = document.querySelector("#taglist")
function tagTyped(event){
	console.log(tagList.value)
	if(event.key != "," || event.target.value.length < 3)
		return
	var elm = document.createElement("span")
	elm.innerHTML = event.target.value.replace(",", "")
	event.target.value = ""
	if (tags.find(f => {return f == elm.innerHTML}))
		return
	elm.addEventListener("click", destroyTag)
	event.target.dispatchEvent(new Event('change'))
	tagList.appendChild(elm)
}

function saveTagField(event){
	grecaptcha.ready(function() {
		grecaptcha.execute('6LfKuH0UAAAAAJpKGjX7auo3dbt29wtjm4_FtATC')
			.then(function(token) {
				var o = {}
				var arr = []
				tagList.querySelectorAll("span").forEach(f => {arr.push(f.innerHTML)})
				o["tags"] = arr
				o["g-recaptcha-response"] = token
				transmit(document.location, o).then(d => translate(d), method="post")
				event.target.classList.remove("show")
			});
	});
}

function destroyTag(event){
	tagList.dispatchEvent(new Event('change'))
	event.target.remove()
}

function FieldUpdatedMessage(data){
	console.log(data)
	displayMessage(data.displayMessage)
	for(var i in data.fields){
		if (i == 'images')
			insertImage(data.fields[i])
		else{
			document.querySelector("[name='"+i+"']").value = data.fields[i]
		}
	}
	
}

function userImage({src, image_id}){
	el = document.createElement("img")
	el.src = src
	el.setAttribute("image_id", image_id)
	el.addEventListener("click", previewImage)
	el.classList.add("usr_img");
	return el;
}

function deleteImage(event){
	id = document.querySelector(".preview[src]").getAttribute("image_id")
	transmit(window.location+"/delimg/"+id).then(t => {translate(t)})
}