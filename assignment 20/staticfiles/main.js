const ws = new WebSocket('ws://127.0.0.1:8000/ws/office/');

ws.onopen = function (e) {
    console.log("Connected to WebSocket server");
    ws.send("Hello Server!");
};

ws.onmessage = function (event) {
    console.log("Message from server:", event.data);
    ws.send("Hello Server!");
};

ws.onclose = function (event) {
    console.log("Connection closed");
};

ws.onerror = function (error) {
    console.log("Error:", error);
};