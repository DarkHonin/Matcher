function edit_profile(event){

}

function update_telemetry(){
	console.log("Starting state update")
	transmit("/home", {}, "INFO").then( data => {translate(data)})
	console.log("Update ended")
}

setInterval(update_telemetry, 15000)
update_telemetry()