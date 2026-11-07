
var websocket = new WebSocket("ws://127.0.0.1:8000/ws/chat/");

websocket.onopen = function (event) {
    console.log("WebSocket connection established:" + event);

    websocket.send("Hello Django Channels!");
};

websocket.onmessage = function (event) {
    console.log("Message received from server: " + event.data);
};

websocket.onclose = function (event) {
    console.log("WebSocket connection closed.");
};

websocket.onerror = function (error) {
    console.error("WebSocket error:", error);
};
