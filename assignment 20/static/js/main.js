
const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";

// Establish a WebSocket connection with the chat server
const chatSocket = new WebSocket(
    `${protocol}//${window.location.host}/ws/chat/general/`
);

// Get the required DOM elements
const form = document.getElementById("form");
const message_input = document.getElementById("message-input");
const send_button = document.getElementById("send-button");
const connection_status = document.getElementById("connection-status");

// Set the initial button state
send_button.disabled = true;


// Handle successful WebSocket connection
chatSocket.onopen = function () {

    // Display connection status in the console
    console.log("WebSocket Connected");

    // Update the connection status in the UI
    connection_status.textContent = "Online";
    connection_status.className = "text-success mt-2 d-block";

    // Enable the send button
    send_button.disabled = false;
};


// Handle messages received from the WebSocket server
chatSocket.onmessage = function (event) {

    // Convert the received JSON string into a JavaScript object
    const data = JSON.parse(event.data);

    // Display the complete received data
    console.log("Received:", data);

    // Handle chat history messages
    if (data.type === "chat_history") {

        // Get all previous messages from the server
        const messages = data.messages;

        // Display previous messages in the console
        console.log("Chat History:", messages);

    }

    // Handle newly received chat messages
    else if (data.type === "chat_message") {

        // Extract the message object
        const message_data = data.message;

        // Display the received message
        console.log("New Message:", message_data);

    }

    // Handle error messages received from the server
    else if (data.type === "error") {

        // Display the server error
        console.error("Server Error:", data.error);

    }
};


// Handle WebSocket connection errors
chatSocket.onerror = function (error) {

    // Display the WebSocket error in the console
    console.error("WebSocket Error:", error);

    // Update the connection status in the UI
    connection_status.textContent = "Connection Error";
    connection_status.className = "text-danger mt-2 d-block";
};


// Handle WebSocket disconnection
chatSocket.onclose = function (event) {

    // Display disconnection information
    console.log("WebSocket Disconnected");
    console.log("Close Code:", event.code);
    console.log("Close Reason:", event.reason);

    // Update the connection status in the UI
    connection_status.textContent = "Offline";
    connection_status.className = "text-danger mt-2 d-block";

    // Disable the send button
    send_button.disabled = true;
};


// Handle message form submission
form.addEventListener("submit", function (event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the message and remove unnecessary whitespace
    const message = message_input.value.trim();

    // Send the message to the WebSocket server
    chatSocket.send(JSON.stringify({message: message}));

    // Display the sent message in the console
    console.log("Sent:", message);

    // Clear the message input field
    message_input.value = "";

});
