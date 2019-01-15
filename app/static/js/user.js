
function updateLikeButton(text){
	if(text == "Unlike"){
		likeBTN.classList.remove("ok")
		likeBTN.classList.add("notok")
	}else if(text == "Like"){
		likeBTN.classList.add("ok")
		likeBTN.classList.remove("notok")
	}

	likeBTN.innerHTML = text
}

function nextIcon(event){
	parent = event.target.parentNode
	current = parent.querySelector(".show")
	if(!current || !current.nextSibling){
		parent.firstChild.classList.add("show")
	}else{
		if (!current.nextSibling.classList)
			return
		current.nextSibling.classList.add("show")
	}
}

function like(event){
	transmit(window.location + "/like", {}).then(f => {translate(f)})
}

function block(event){
	transmit(window.location + "/block", {}).then(f => {translate(f)})
}

function blocking(el, data){
	el.innerHTML = data
}

function has_been_liked(){
	el = document.createElement("label")
	el.classList.add("ul")
	el.classList.add("ok")
	el.innerHTML = "Liked!"
	return el
}