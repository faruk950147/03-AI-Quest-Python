const ws = new WebSocket('ws://127.0.0.1:8000/ws/office/');

ws.onopen = function (e) {
    console.log("Connected to WebSocket server");
    document.getElementById('connection-status').innerHTML = 'Connected';
    ws.send("Hello Server!");
};

ws.onmessage = function (event) {
    console.log("Message from server:", event.data);
    document.getElementById('message-status').innerHTML += 'Receiver: ' + event.data + '<br>';
    ws.send("Hello Server!");
};

ws.onclose = function (event) {
    console.log("Connection closed");
    document.getElementById('connection-status').innerHTML = 'Disconnected';
};

ws.onerror = function (error) {
    console.log("Error:", error);
    document.getElementById('error-status').innerHTML = 'Error occurred';
};