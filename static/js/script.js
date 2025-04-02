//function userJoined(username) {
//  console.log(`${username} has joined the room.`);
//  // You can also update the chat UI here
//  document.getElementById('chat-log').innerHTML += `<p>${username} has joined the room.</p>`;
//}

//var socketio = io();
//
//const messages = document.getElementById('messages');
//
//const createMessage = (username, msg) => {
//    const content = `
//    <div class="text>
//        <span>
//            <strong>${username}</strong>: ${msg}
//        </span>
//        <span class="muted">
//            ${new Date().toLocaleTimeString()}
//        </span>
//    </div>
//    `;
//    messages.innerHTML += content;
//};

socketio.on('message', (data) => {
     createMessage(data.username, data.message);
 });