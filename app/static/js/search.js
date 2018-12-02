const options = document.querySelector("#searchbar>select")
const list = document.querySelector(".search>ul")

function search(event){
	data = {}
	data[event.target.parentNode.querySelector("select").value] = event.target.value
	list.classList.add("empty")
	list.querySelectorAll(".item").forEach(f => f.remove())
	transmit("/search", data).then( f=>translate(f))
}


function setPlaceholder(event){
	opt = options.options[options.selectedIndex]
	event.target.parentNode.querySelector("input").setAttribute("placeholder", opt.getAttribute("placeholder"))
}

const parser = new DOMParser();

function showResult(data){
	console.log(data)
	data.forEach(item => {
		var cc = '<li class="item"><span>uname</span><span>lname</span><span>fname</span><span>age</span><span>fame</span></li>'
		console.log(item)
		for (i in item){
			cc = cc.replace(i, item[i])
		}
		frag = parser.parseFromString(cc, 'text/html')
		console.log(frag)
		list.appendChild(frag.body.firstChild)
	})
	list.classList.remove("empty")
}