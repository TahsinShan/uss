const socket = io(window.location.origin, {
    transports: ["websocket", "polling"]
});

function sendMessage() {
    let msgInput = document.getElementById("message");
    let msg = msgInput.value.trim();
    if (msg) {
        socket.send(msg);
        msgInput.value = "";
    }
}

document.getElementById("send").onclick = sendMessage;

document.getElementById("message").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
});

socket.on("message", (data) => {
    let messagesDiv = document.getElementById("messages");

    let username, message;
    if (typeof data === "object" && data.username && data.message) {
        username = data.username;
        message = data.message;
    } else {
        username = "Server";
        message = data;
    }

    messagesDiv.innerHTML += `<p class="chat-msg"><strong>${username}:</strong> ${message}</p>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});
