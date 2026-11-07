
var websocket = new WebSocket("ws://localhost:8000/ws/chat/");

/* 
websocket.onopen = function (event) {
    console.log("WebSocket connection established:" + event);

    websocket.send("Hello Django Channels!");
};

websocket.onmessage = function (event) {
    console.log("Message received from server: " + event.data);
    document.getElementById("display").innerHTML += event.data;
};

websocket.onclose = function (event) {
    console.log("WebSocket connection closed.");
};

websocket.onerror = function (error) {
    console.error("WebSocket error:", error);
};
 
*/

websocket.addEventListener('open', function (event) {
    console.log("WebSocket connection established:" + event);

    websocket.send("Hello Django Channels!");
});

websocket.addEventListener('message', function (event) {
    console.log("Message received from server: " + event.data);
    document.getElementById("display").innerHTML += event.data;
});

websocket.addEventListener('close', function (event) {
    console.log("WebSocket connection closed.");
});

websocket.addEventListener('error', function (error) {
    console.error("WebSocket error:", error);
});





