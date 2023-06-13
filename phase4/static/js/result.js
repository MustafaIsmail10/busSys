function displayFunc(msg){
    window.location.href = "/result/";
    //window.open("http://localhost:8000/result/", "_self");
    console.log("in resulttt :", msg.result);
    var d = document.getElementById("res");
    d.innerText = msg;
    // const resultsContainer = document.createElement("div");
    // resultsContainer.textContent = msg.result;
    // d.appendChild(resultsContainer);
}