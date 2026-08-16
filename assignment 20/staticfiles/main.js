const chatLog = document.getElementById("chat-log");
const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

// Get room name
const roomName = JSON.parse(document.getElementById('room-name').textContent);

// Protocol detect
const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';

// WebSocket connect
const socket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${roomName}/`);

// Connection opened
socket.onopen = function (e) {
    console.log("WebSocket connected:", e);
};

// Message received → UI 
socket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    console.log("Message received:", data);

    // textarea message append
    chatLog.value += data.message + '\n';

    // auto scroll to bottom
    chatLog.scrollTop = chatLog.scrollHeight;
};

// Error
socket.onerror = function (e) {
    console.error("WebSocket error:", e);
};

// Close
socket.onclose = function () {
    console.log("WebSocket closed");
};

// Send message
sendBtn.onclick = function () {
    const message = input.value.trim();

    if (message === '') return;

    socket.send(JSON.stringify({
        'message': message
    }));

    input.value = '';
};

// Enter press = send
input.addEventListener("keyup", function (e) {
    if (e.key === "Enter") {
        sendBtn.click();
    }
});