const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";

// WebSocket Connection
const chatSocket = new WebSocket(
    `${protocol}//${window.location.host}/ws/chat/general/`
);

// DOM Elements
const message_input = document.getElementById("message-input");
const send_button = document.getElementById("send-button");
const connection_status = document.getElementById("connection-status");

// Initial State
send_button.disabled = true;


// WebSocket Connected
chatSocket.onopen = function () {
    console.log("WebSocket Connected");

    connection_status.textContent = "Online";
    connection_status.className = "text-success mt-2 d-block";

    send_button.disabled = false;
};

// Receive WebSocket Messages
chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    console.log("Received:", data);
};

// WebSocket Error
chatSocket.onerror = function (error) {
    console.error("WebSocket Error:", error);

    connection_status.textContent = "Connection Error";
    connection_status.className = "text-danger mt-2 d-block";
};

// WebSocket Disconnected
chatSocket.onclose = function (event) {
    console.log("WebSocket Disconnected");
    console.log("Close Code:", event.code);
    console.log("Close Reason:", event.reason);

    connection_status.textContent = "Offline";
    connection_status.className = "text-danger mt-2 d-block";

    send_button.disabled = true;
};

// Send Message
send_button.addEventListener("click", function () {
    const message = message_input.value.trim();

    if (!message) return;

    chatSocket.send(JSON.stringify({
        message: message
    }));

    console.log("Sent:", message);

    message_input.value = "";
});


