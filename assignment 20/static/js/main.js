
const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";

const chatSocket = new WebSocket(
    `${protocol}//${window.location.host}/ws/chat/general/`
);


// DOM Elements
const form = document.getElementById("form");
const message_input = document.getElementById("message-input");
const send_button = document.getElementById("send-button");
const connection_status = document.getElementById("connection-status");
const chat_messages = document.getElementById("chat-messages");


// Initial State
send_button.disabled = true;


// Connection Status
function updateStatus(message, className) {

    connection_status.textContent = message;
    connection_status.className = `${className} d-block`;

}


// Enable / Disable Send Button
function updateSendButton() {

    send_button.disabled = (
        !message_input.value.trim() ||
        chatSocket.readyState !== WebSocket.OPEN
    );

}


// Scroll to Bottom
function scrollToBottom() {

    chat_messages.scrollTop = chat_messages.scrollHeight;

}


// Create Message
function createMessage(message) {

    const isOwnMessage =
        String(message.user_id) === String(CURRENT_USER_ID);


    // Message Wrapper
    const wrapper = document.createElement("div");

    wrapper.className = isOwnMessage
        ? "d-flex justify-content-end mb-3"
        : "d-flex justify-content-start mb-3";


    // Message Bubble
    const bubble = document.createElement("div");

    bubble.className = isOwnMessage
        ? "bg-primary text-white rounded-4 p-3"
        : "bg-secondary text-white rounded-4 p-3";

    bubble.style.maxWidth = "75%";
    bubble.style.minWidth = "100px";


    // Message Header
    const header = document.createElement("div");

    header.className = "d-flex align-items-center gap-2 mb-2";


    // Username
    const username = document.createElement("strong");

    username.className = isOwnMessage
        ? "text-light"
        : "text-info";

    username.textContent = isOwnMessage
        ? "You"
        : message.username;


    // Time
    const time = document.createElement("small");

    time.className = "text-white-50";
    time.textContent = message.created_at;


    // Message Content
    const content = document.createElement("div");

    content.className = "text-break";
    content.textContent = message.content;


    // Append Elements
    header.appendChild(username);
    header.appendChild(time);

    bubble.appendChild(header);
    bubble.appendChild(content);

    wrapper.appendChild(bubble);


    return wrapper;

}


// Empty Message
function showEmptyMessage() {

    const empty = document.createElement("div");

    empty.className = "text-center text-secondary mt-5";

    empty.textContent = "No messages yet. Start a conversation!";

    chat_messages.replaceChildren(empty);

}


// Render Chat History
function renderChatHistory(messages) {

    chat_messages.replaceChildren();

    if (!messages || messages.length === 0) {

        showEmptyMessage();
        return;

    }

    const fragment = document.createDocumentFragment();

    messages.forEach(function (message) {

        fragment.appendChild(createMessage(message));

    });

    chat_messages.appendChild(fragment);

    scrollToBottom();

}


// Render New Message
function renderNewMessage(message) {

    // Remove empty message
    if (chat_messages.querySelector(".text-secondary.mt-5")) {

        chat_messages.replaceChildren();

    }

    chat_messages.appendChild(createMessage(message));

    scrollToBottom();

}


// WebSocket Connected
chatSocket.onopen = function () {

    console.log("WebSocket Connected");

    updateStatus("Online", "text-success");

    updateSendButton();

};


// Receive Messages
chatSocket.onmessage = function (event) {

    const data = JSON.parse(event.data);

    console.log("Received:", data);


    // Chat History
    if (data.type === "chat_history") {

        renderChatHistory(data.messages);

    }


    // New Message
    else if (data.type === "chat_message") {

        renderNewMessage(data.message);

    }


    // Server Error
    else if (data.type === "error") {

        console.error("Server Error:", data.error);

    }

};


// WebSocket Error
chatSocket.onerror = function (error) {

    console.error("WebSocket Error:", error);

    updateStatus("Connection Error", "text-danger");

    updateSendButton();

};


// WebSocket Disconnected
chatSocket.onclose = function (event) {

    console.log("WebSocket Disconnected");
    console.log("Close Code:", event.code);
    console.log("Close Reason:", event.reason);

    updateStatus("Offline", "text-danger");

    updateSendButton();

};


// Send Message
form.addEventListener("submit", function (event) {

    event.preventDefault();

    const message = message_input.value.trim();

    if (!message || chatSocket.readyState !== WebSocket.OPEN) {

        return;

    }

    chatSocket.send(JSON.stringify({

        message: message

    }));

    console.log("Sent:", message);

    message_input.value = "";

    updateSendButton();

});


// Input Event
message_input.addEventListener("input", updateSendButton);

