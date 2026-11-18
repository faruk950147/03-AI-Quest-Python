
const protocol = window.location.protocol === "https:"
    ? "wss:"
    : "ws:";

// WebSocket Connection
const chatSocket = new WebSocket(
    `${protocol}//${window.location.host}/ws/chat/general/`
);

// DOM Elements
const message_input = document.getElementById("message-input");
const send_button = document.getElementById("send-button");
const chat_messages = document.getElementById("chat-messages");
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

    try {
        const data = JSON.parse(event.data);

        console.log("Received:", data);

        // Chat History
        if (data.type === "chat_history") {

            chat_messages.innerHTML = "";

            data.messages.forEach(function (message) {
                displayMessage(message, "received");
            });

        }

        // New Chat Message
        else if (data.type === "chat_message") {

            displayMessage(data.message, "received");

        }

        // Error Message
        else if (data.type === "error") {

            console.error("Server Error:", data.error);

            alert(data.error);

        }

        else {
            console.warn("Unknown message type:", data);
        }

    } catch (error) {
        console.error("Message Parsing Error:", error);
    }
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


// Display Message
function displayMessage(message, type) {

    const messageElement = document.createElement("div");

    messageElement.classList.add(
        "message",
        type === "sent" ? "text-end" : "text-start"
    );

    const messageText = document.createElement("div");

    messageText.classList.add(
        "d-inline-block",
        "p-2",
        "rounded",
        "mb-2"
    );

    if (type === "sent") {
        messageText.classList.add("bg-primary", "text-white");
    } else {
        messageText.classList.add("bg-secondary", "text-white");
    }

    // Username
    if (message.username) {

        const username = document.createElement("small");

        username.classList.add("d-block", "fw-bold");

        username.textContent = message.username;

        messageText.appendChild(username);
    }

    // Message Content
    const content = document.createElement("span");

    content.textContent = message.content || "";

    messageText.appendChild(content);

    // Append Message
    messageElement.appendChild(messageText);

    chat_messages.appendChild(messageElement);

    // Auto Scroll
    chat_messages.scrollTop = chat_messages.scrollHeight;
}


// Send Message
function sendMessage() {

    const message = message_input.value.trim();

    if (!message) {
        return;
    }

    if (chatSocket.readyState === WebSocket.OPEN) {

        chatSocket.send(JSON.stringify({
            message: message
        }));

        // Clear Input
        message_input.value = "";

        message_input.focus();

    } else {

        console.log("WebSocket is not connected!");

    }
}


// Send Button Click
send_button.addEventListener("click", sendMessage);


// Enter Key Send
message_input.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }

});
