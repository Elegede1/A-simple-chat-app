// This file contains common chat functionality
// The specific room initialization will be done in the template

let socket;
let messageContainer;
let messageInput;
let sendButton;
let username;
let roomCode;

// Initialize chat functionality
function initializeChat(user, room) {
    socket = io();
    messageContainer = document.getElementById('message-container');
    messageInput = document.getElementById('message-input');
    sendButton = document.getElementById('send-btn');
    username = user;
    roomCode = room;
    
    // Join the room when the page loads
    socket.on('connect', () => {
        // Emit join_room event
        socket.emit('join_room', {
            username: username,
            room: roomCode
        });
    });
    
    // Handle incoming messages
    socket.on('message', (data) => {
        displayMessage(data);
    });
    
    // Send message when button is clicked
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    // Send message when Enter key is pressed
    if (messageInput) {
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
}

function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('message', {
            msg: message
        });
        messageInput.value = '';
    }
}

function displayMessage(data) {
    const messageElement = document.createElement('div');
    
    if (data.username === 'System') {
        // Style system messages differently
        messageElement.classList.add('system-message');
        messageElement.textContent = data.msg;
        
        if (data.timestamp) {
            const timestamp = document.createElement('span');
            timestamp.classList.add('timestamp');
            timestamp.textContent = data.timestamp;
            messageElement.appendChild(timestamp);
        }
    } else {
        // Regular user message
        messageElement.classList.add('user-message');
        const content = document.createElement('span');
        content.textContent = `${data.username}: ${data.msg}`;
        messageElement.appendChild(content);
        
        if (data.timestamp) {
            const timestamp = document.createElement('span');
            timestamp.classList.add('timestamp');
            timestamp.textContent = data.timestamp;
            messageElement.appendChild(timestamp);
        }
    }
    
    messageContainer.appendChild(messageElement);
    
    // Auto-scroll to the bottom
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

// Function to display existing messages (called from the template)
function displayExistingMessage(username, msg, timestamp) {
    displayMessage({
        username: username,
        msg: msg,
        timestamp: timestamp
    });
}
