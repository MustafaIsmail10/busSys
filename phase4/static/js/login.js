const socket = new WebSocket('ws://localhost:1445/ws');


const makeRandColor = () => {
    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    return `rgb(${r}, ${g}, ${b})`;
}

socket.addEventListener('open', function(event) {
    console.log('WebSocket connection opened:', event);
    socket.send('login admin admin');
});

socket.addEventListener('message', function(event) {
    if (event.data != 'null'){
        console.log('WebSocket message received:', event.data);
        // socket.send("get_maps");
	}
});

socket.addEventListener('close', function(event) {
    console.log('WebSocket connection closed:', event);
});

socket.addEventListener('error', function(event) {
    console.error('WebSocket error:', event);
});

// // Send a message to the server every second
// setInterval(function() {
//     socket.send('Ping');
// }, 5000);