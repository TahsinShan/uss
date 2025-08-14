const socket = io();

function sendMessage() {
    let msgInput = document.getElementById("message");
    let msg = msgInput.value;
    if (msg.trim()) {
        socket.send(msg);
        msgInput.value = "";
    }
}

document.getElementById("send").onclick = sendMessage;

// Send message when pressing Enter
document.getElementById("message").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault(); // prevent newline in input
        sendMessage();
    }
});

socket.on("message", (data) => {
    let messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += `<p><strong>${data.username}:</strong> ${data.message}</p>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});
