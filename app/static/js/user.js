function like(event){
	transmit(document.location, {}, "LIKE").then(f => translate(f))	
}

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