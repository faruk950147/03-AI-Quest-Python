

















































document.addEventListener("DOMContentLoaded", function () {

    const send_btn = document.getElementById("send-button");
    const message_input = document.getElementById("message-input");
    const chat_messages = document.getElementById("chat-messages");

    const roomName = "room1";

    const chatSocket = new WebSocket(
        "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
    );

    // Connected
    chatSocket.onopen = function () {
        console.log("WebSocket connected!");
    };

    // Receive Message
    chatSocket.onmessage = function (event) {

        try {
            const data = JSON.parse(event.data);

            const messageElement = document.createElement("p");
            messageElement.textContent = data.message;

            chat_messages.appendChild(messageElement);

            chat_messages.scrollTop = chat_messages.scrollHeight;

        } catch (error) {
            console.error("Invalid JSON received:", event.data);
        }
    };

    // Error
    chatSocket.onerror = function (error) {
        console.error("WebSocket error:", error);
    };

    // Closed
    chatSocket.onclose = function (event) {
        console.log("WebSocket closed:", event);
    };

    // Send Message
    function sendMessage() {

        const message = message_input.value.trim();

        if (!message) return;

        if (chatSocket.readyState === WebSocket.OPEN) {

            chatSocket.send(JSON.stringify({
                message: message
            }));

            message_input.value = "";

        } else {
            console.log("WebSocket is not connected!");
        }
    }

    send_btn.addEventListener("click", sendMessage);

    message_input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

});
