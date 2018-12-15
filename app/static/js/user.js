
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
	if(current)
		current.classList.remove("show")
	if(!current || !current.nextSibling){
		parent.firstChild.classList.add("show")
	}else{
		current.nextSibling.classList.add("show")
	}
}
