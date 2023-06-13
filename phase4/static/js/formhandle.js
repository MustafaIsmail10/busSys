let socket;

function showNotification(message) {
    var notificationBox = document.getElementById("notification-box");
    var notificationMessage = document.getElementById("notification-message");
  
    notificationMessage.innerText = message;
    notificationBox.style.display = "block";
  
    setTimeout(function() {
      notificationBox.style.opacity = 1;
    }, 100);
  
    document.addEventListener('click', function(event) {
        notificationBox.style.display = 'none';
      });
  }
  
function connectWebSocket() {
    socket = new WebSocket("ws://localhost:1445/ws");
    socket.onopen = function () {
        const token = localStorage.getItem("token");
        socket.send(`auToken ${token}`);
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
            document.getElementById("page").style.display = "block";
           
        } else if (msg.type == "notification") {
            console.log("result " ,msg);
        } else {
            console.log("result received " ,msg.result);
            showNotification(msg.result);
                      
        }
    };

    socket.onclose = function (event) {
        console.log("WebSocket connection closed with code:", event.code); 
    };
}



connectWebSocket();

var forms = document.querySelectorAll("form");

// Attach an event listener to each form's submit event
forms.forEach(function(form) {
    form.addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission
        console.log("clicked");
    // Get the form data
    var formData = new FormData(form);
    var toserver="";
    // Loop over the form data using a for...of loop
    for (var entry of formData.entries()) {
        var fieldName = entry[0];
        var fieldValue = entry[1];
        if (fieldName == "csrfmiddlewaretoken"){
            continue;
        }
        
        else{
            toserver+= " " + fieldValue ;
        }
    
    }
    socket.send(toserver);
    });
});



