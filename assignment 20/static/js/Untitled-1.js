
const contacts = document.querySelectorAll(".contact");

const chatName = document.getElementById("chatName");
const chatStatus = document.getElementById("chatStatus");
const headerAvatar = document.getElementById("headerAvatar");
const chatApp = document.getElementById("chat-app");

contacts.forEach(contact => {

    contact.addEventListener("click", function () {

        // Remove active class
        contacts.forEach(item => {
            item.classList.remove("active");
        });

        // Add active class
        this.classList.add("active");

        // Get contact information
        const name = this.dataset.name;
        const status = this.dataset.status;

        // Update Chat Header
        chatName.textContent = name;
        chatStatus.textContent = status;

        // Update Avatar
        const initials = name
            .split(" ")
            .map(word => word[0])
            .join("");

        headerAvatar.textContent = initials;

        // Remove old online indicator
        const online = document.createElement("div");

        if (status === "Online") {
            online.classList.add("online");
            headerAvatar.appendChild(online);
        }

        // Clear previous messages
        document.getElementById("messages").innerHTML = "";

        // Mobile sidebar
        chatApp.classList.add("chat-open");

    });

});



const roomName = window.location.pathname.split("/").filter(Boolean).pop();

const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const messages = document.getElementById("messages");

// WebSocket Connection
const protocol = window.location.protocol === "https:" ? "wss" : "ws";

const chatSocket = new WebSocket(
    `${protocol}://${window.location.host}/ws/chat/${roomName}/`
);

// WebSocket Connected
chatSocket.onopen = function () {
    console.log("WebSocket Connected:", roomName);
};

// Receive Message
chatSocket.onmessage = function (event) {

    const data = JSON.parse(event.data);

    const message = data.message;

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "received");

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");

    bubble.appendChild(document.createTextNode(message));

    const time = document.createElement("span");
    time.classList.add("time");

    time.textContent = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    bubble.appendChild(time);
    messageDiv.appendChild(bubble);

    messages.appendChild(messageDiv);

    // Auto Scroll
    messages.scrollTop = messages.scrollHeight;
};

// Send Message
function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) return;

    if (chatSocket.readyState === WebSocket.OPEN) {

        chatSocket.send(JSON.stringify({
            message: message
        }));

        messageInput.value = "";
        messageInput.focus();

    } else {
        console.log("WebSocket is not connected.");
    }
}

// Send Button Click
sendBtn.addEventListener("click", sendMessage);

// Enter Key
messageInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }

});

// WebSocket Error
chatSocket.onerror = function (error) {
    console.error("WebSocket Error:", error);
};

// WebSocket Disconnected
chatSocket.onclose = function () {
    console.log("WebSocket Disconnected");
};