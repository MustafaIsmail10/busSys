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
            document.getElementById("error_msg").innerText = "Invalid username or password"
        } else if (msg.type == "token") {
            console.log(msg.token)
            // Store the token insided the browser and redirect to home page
            localStorage.setItem("token", msg.token);
            // window.open("http://localhost:8000", "_self");
            document.forms[0].innerHTML = "";
            document.getElementById("h2").innerText = "Notifications"
            var els = document.getElementsByClassName("not_logged");
            els[0].innerHTML = msg.username;
            els[0].removeAttribute("href");
            els[1].href = ""
            els[1].innerHTML = "signout";
            els[1].addEventListener("click", (e) => {
                localStorage.setItem("token", "");
            })
            document.getElementById("error_msg").innerText = ""


        } else if (msg.type == "notification") {
            console.log(msg)
            for (let r of msg.result){
                new_element = document.createElement("div")
                console.log(r)
                new_element.innerText = r
                document.getElementById("notifications").appendChild(new_element)
            }
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



const login_form = document.forms[0]
login_form.addEventListener("submit", (e) => {
    e.preventDefault();
    socket.send(`login ${login_form.username.value} ${login_form.password.value}`)
    console.log(login_form.username.value, login_form.password.value);
})



// function connectWebSocket() {
//     socket = new WebSocket('ws://localhost:1445/ws');
// }

// socket.addEventListener('open', function (event) {
//     console.log('WebSocket connection opened:', event);
// });

// socket.addEventListener('message', function (event) {
//     if (event.data != 'null') {
//         console.log('WebSocket message received:', event.data);
//         // socket.send("get_maps");
//     }
// });

// socket.addEventListener('close', function (event) {
//     console.log('WebSocket connection closed:', event);
// });

// socket.addEventListener('error', function (event) {
//     console.error('WebSocket error:', event);
// });

// // Send a message to the server every second
// setInterval(function() {
//     socket.send('Ping');
// }, 5000);