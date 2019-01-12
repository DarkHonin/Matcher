function sliderUpdate(event){
	var val = event.target.value
	if (val < 0){
		event.target.parentNode.setAttribute("data-value", "Unset")
	}else
		event.target.parentNode.setAttribute("data-value", val)

}