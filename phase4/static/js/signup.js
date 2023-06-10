let socket;

function connectWebSocket() {
    socket = new WebSocket("ws://localhost:1445/ws");
    socket.onopen = function () {
        console.log("WebSocket connection established");
    };

    socket.onmessage = function (event) {
        console.log("Received message:", event.data);
        let msg = JSON.parse(event.data)

        if (msg.type == "error") {
            document.getElementById("error_msg").innerText = "Try different username"
        } else if (msg.type == "token") {
            console.log(msg.token)
            // Store the token insided the browser and redirect to home page
            localStorage.setItem("token", msg.token);
            window.open("http://localhost:8000", "_self");
            document.getElementById("error_msg").innerText = ""
        
        } else if (msg.type == "notification") {

        } else {

        }
    };

    socket.onclose = function (event) {
        console.log("WebSocket connection closed with code:", event.code);
        console.log("Attempting to reopen the connection...");

        // Attempt to reopen the connection after a delay
        setTimeout(connectWebSocket, 500);
    };
}

connectWebSocket();



const signup_form = document.forms[0]
signup_form.addEventListener("submit", (e) => {
    e.preventDefault();
    socket.send(`register ${signup_form.username.value} ${signup_form.password.value}`)
    console.log(signup_form.username.value, signup_form.password.value);
})
