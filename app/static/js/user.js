const socket = io.connect('http://' + document.domain + ':' + location.port + "/user_transmissions");

socket.on('connect', function() {
    
});