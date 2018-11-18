document.querySelectorAll(".controler").forEach(i => {
	var trigger = i.getAttribute("trigger");
	var action = i.getAttribute("action");
	i.addEventListener(trigger, action);
})