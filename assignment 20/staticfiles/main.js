const chatBox = document.getElementById("chat-log");
const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");
console.log('window', window);
console.log('window.location', window.location);
console.log('window.location.hostname', window.location.hostname);

const socket = new WebSocket("ws://" + window.location.hostname + ":8000/ws/chat/");

// Connection opened
socket.onopen = function () {
    console.log("WebSocket connected");
};

// Receive message
socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    // append as plain text with a line break
    chatBox.innerHTML += data.message + "\n";
    chatBox.scrollTop = chatBox.scrollHeight; // auto scroll
};
// Error handling
socket.onerror = function (error) {
    console.log("WebSocket error:", error);
};

// Connection closed
socket.onclose = function () {
    console.log("WebSocket closed");
};

// Send message on button click
sendBtn.addEventListener("click", function (e) {
    e.preventDefault();
    if (input.value.trim() === "") return; // prevent empty messages
    socket.send(JSON.stringify({ message: input.value }));
    input.value = "";
});

// Send message on Enter key
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendBtn.click();
});