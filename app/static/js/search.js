const tagList = document.querySelector("#taglist")
const tagHolder = document.querySelector("#tagsHolder")

if (tagHolder.value){
	console.log("current val: ", tagHolder.value)
	tagHolder.arr = tagHolder.value.split(", ")
	console.log("Arr: ", tagHolder.arr)
}

function sliderUpdate(event){
	var val = event.target.value
	if (val < 0){
		event.target.parentNode.setAttribute("data-value", "Unset")
	}else
		event.target.parentNode.setAttribute("data-value", val)
}

function tagEventListner(event){
	if (event.key == ","){
		// Fancy things
		event.target.value = event.target.value.replace(",", "")
		el = document.createElement("span")
		el.innerHTML = event.target.value
		el.addEventListener("click", tagRemove)
		if ( !tagHolder["arr"] )
			tagHolder["arr"] = []
		tagHolder.arr.push(el.innerHTML)
		tagHolder.value = tagHolder.arr.join(", ")
		tagList.appendChild(el)
		event.target.value = ""
	}
	console.log(tagHolder.arr)
}

function tagRemove(event){
	tagHolder.arr.splice(tagHolder.arr.indexOf(event.target.innerHTML), 1)
	tagHolder.value = tagHolder.arr.join(", ")
	event.target.remove()
}