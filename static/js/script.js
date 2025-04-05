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
    // Create message wrapper
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message';

    if (data.username === 'System') {
        // System message
        messageWrapper.className = 'system-message-container';

        const systemBubble = document.createElement('div');
        systemBubble.className = 'system-message-bubble';
        systemBubble.textContent = data.msg;

        messageWrapper.appendChild(systemBubble);

        if (data.timestamp) {
            const timestamp = document.createElement('div');
            timestamp.className = 'timestamp';
            timestamp.textContent = data.timestamp;
            systemBubble.appendChild(timestamp);
        }
    } else {
        // User message
        const isCurrentUser = data.username === username;

        // Create message bubble
        const messageBubble = document.createElement('div');
        messageBubble.className = `user-message ${isCurrentUser ? 'my-message' : 'other-user-message'}`;

        // Only show username for other users' messages
        if (!isCurrentUser) {
            const usernameElement = document.createElement('div');
            usernameElement.className = 'username';
            usernameElement.textContent = data.username;
            messageBubble.appendChild(usernameElement);
        }

        // Message content
        const content = document.createElement('div');
        content.className = 'content';
        content.textContent = data.msg;
        messageBubble.appendChild(content);

        // Timestamp
        if (data.timestamp) {
            const timestamp = document.createElement('div');
            timestamp.className = 'timestamp';
            timestamp.textContent = data.timestamp;
            messageBubble.appendChild(timestamp);
        }

        messageWrapper.appendChild(messageBubble);
    }

    messageContainer.appendChild(messageWrapper);
    
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
