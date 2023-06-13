let socket;




function showNotification(message) {
    var notificationBox = document.getElementById("notification-box");
    var notificationMessage = document.getElementById("notification-message");

    notificationMessage.innerText = message;
    notificationBox.style.display = "block";

    setTimeout(function () {
        notificationBox.style.opacity = 1;
    }, 100);

    document.addEventListener('click', function (event) {
        notificationBox.style.display = 'none';
    });
}



function connectWebSocket() {
    socket = new WebSocket("ws://localhost:1445/ws");
    socket.onopen = function () {
        const token = localStorage.getItem("token");
        socket.send(`auToken ${token}`)
    };

    socket.onmessage = function (event) {
        console.log("Received message:", event.data);
        let msg = JSON.parse(event.data)

        if (msg.type == "error") {
            window.open("http://localhost:8000/login", "_self");
        } else if (msg.type == "token") {
            var els = document.getElementsByClassName("not_logged");

            els[0].innerHTML = msg.username;
            els[0].removeAttribute("href");
            els[1].href = ""
            els[1].innerHTML = "signout";
            els[1].addEventListener("click", (e) => {
                localStorage.setItem("token", "");
            });
            console.log(document.getElementById("options"));
            document.getElementById("options").style.display = "block";

        }
        else if (msg.type == "notification") {
            showNotification(msg.result);
        } else {

        }
    };

    socket.onclose = function (event) {
        console.log("WebSocket connection closed with code:", event.code);
        document.getElementById("options").style.display = "none";
    };
}


connectWebSocket();

