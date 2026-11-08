
const roomName = "room1";

const chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);

chatSocket.onopen = function (event) {
    console.log("WebSocket connected!");
};

chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);

};

chatSocket.onclose = function (event) {
    console.log("WebSocket disconnected!");
};

chatSocket.onerror = function (error) {
    console.error("WebSocket error:", error);
};
