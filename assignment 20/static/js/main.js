const protocol = window.location.protocol === "https:"
    ? "wss:"
    : "ws:";

const chatSocket = new WebSocket(
    `${protocol}//${window.location.host}/ws/chat/general/`
);

const message_input = document.getElementById("message-input");
const send_button = document.getElementById("send-button");
const chat_messages = document.getElementById("chat-messages");
const connection_status = document.getElementById("connection-status");

chatSocket.onopen = function (event) {
    console.log("Online");
    connection_status.textContent = "Online";
    connection_status.className = "text-success mt-2 d-block";
};

chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log("Message:", data.message);
};

chatSocket.onerror = function (error) {
    console.error("Connection error:", error);
    connection_status.textContent = "Connection error";
    connection_status.className = "text-danger mt-2 d-block";
};

chatSocket.onclose = function (event) {
    console.log("Offline");
    console.log("Close code:", event.code);
    console.log("Close reason:", event.reason);
    connection_status.textContent = "Offline";
    connection_status.className = "text-danger mt-2 d-block";
};
