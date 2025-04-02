from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort, session
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from string import ascii_uppercase
import random
import os
from dotenv import load_dotenv
import datetime
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# Configure MongoDB
app.config['MONGO_URI'] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Track active rooms in memory (room details will be in MongoDB)
active_rooms = {}
connected_users = {}


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        # Check if room code exists in MongoDB
        if not mongo.db.rooms.find_one({"code": code}):
            break

    return code

# Create indexes (run this once)
def create_indexes():
    mongo.db.rooms.create_index("code", unique=True)
    mongo.db.messages.create_index([("room_code", 1), ("timestamp", 1)])

# Call this function when your app starts
create_indexes()



@socketio.on('connect')
def handle_connect():
    create_indexes()
    print("Client connected")


@socketio.on('join_room')
def handle_join_room(data):
    room_code = data['room']
    username = data['username']
    user_id = request.sid

    # Check if room exists in MongoDB
    room = mongo.db.rooms.find_one({"code": room_code})
    if not room:
        return

    # Join the Socket.IO room
    join_room(room_code)

    # Track user connection
    is_new_join = True
    if room_code in connected_users:
        if username in connected_users[room_code]:
            # User refreshed the page
            is_new_join = False
            connected_users[room_code][username] = user_id
        else:
            # New user joined
            connected_users[room_code][username] = user_id
    else:
        # First user in room
        connected_users[room_code] = {username: user_id}

    # Only send join message if this is a new join
    if is_new_join:
        # Create system message
        message = {
            "room_code": room_code,
            "username": "System",
            "content": f"{username} has joined the room",
            "timestamp": datetime.datetime.utcnow()
        }

        # Save to MongoDB
        mongo.db.messages.insert_one(message)

        # Send to all users in room
        emit('message', {
            'msg': message["content"],
            'username': message["username"],
            'timestamp': message["timestamp"].strftime("%I:%M:%p")
        }, to=room_code)

        # Update member count in MongoDB
        mongo.db.rooms.update_one(
            {"code": room_code},
            {"$inc": {"member_count": 1}}
        )


@socketio.on('message')
def handle_message(data):
    room_code = session.get('room')
    username = session.get('username')

    if not room_code or not username:
        return

    # Create message document
    message = {
        "room_code": room_code,
        "username": username,
        "content": data['msg'],
        "timestamp": datetime.datetime.utcnow()
    }

    # Save to MongoDB
    mongo.db.messages.insert_one(message)

    # Send to all users in room
    emit('message', {
        'msg': message["content"],
        'username': message["username"],
        'timestamp': message["timestamp"].strftime("%I:%M:%p")
    }, to=room_code)


@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    room_code = session.get('room')
    username = session.get('username')

    if not room_code or not username:
        return

    # Check if this is a true disconnect
    is_true_disconnect = False
    if room_code in connected_users and username in connected_users[room_code]:
        if connected_users[room_code][username] == user_id:
            # Remove user from tracking
            del connected_users[room_code][username]
            is_true_disconnect = True

            if len(connected_users[room_code]) == 0:
                del connected_users[room_code]

    if is_true_disconnect:
        # Create system message
        message = {
            "room_code": room_code,
            "username": "System",
            "content": f"{username} has left the room",
            "timestamp": datetime.datetime.utcnow()
        }

        # Save to MongoDB
        mongo.db.messages.insert_one(message)

        # Send to all users in room
        emit('message', {
            'msg': message["content"],
            'username': message["username"],
            'timestamp': message["timestamp"].strftime("%H:%M:%S")
        }, to=room_code)

        # Update member count in MongoDB
        mongo.db.rooms.update_one(
            {"code": room_code},
            {"$inc": {"member_count": -1}}
        )

        # Check if room is empty
        room = mongo.db.rooms.find_one({"code": room_code})
        if room and room.get("member_count", 0) <= 0:
            # Optional: Delete room or mark as inactive
            # mongo.db.rooms.delete_one({"code": room_code})
            pass


@app.route('/', methods=['GET', 'POST'])
def index():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        code = request.form['code']
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        if not username:
            return render_template('index.html', error="Please enter a username.", username=username, code=code)

        if join and not code:
            return render_template('index.html', error="Please enter a room code.", username=username, code=code)

        if create:
            # Generate a new room code
            room_code = generate_unique_code(4)

            # Create room in MongoDB
            room = {
                "code": room_code,
                "created_at": datetime.datetime.utcnow(),
                "member_count": 0
            }
            mongo.db.rooms.insert_one(room)
        else:
            room_code = code
            # Check if room exists
            if not mongo.db.rooms.find_one({"code": room_code}):
                return render_template('index.html', error="Room does not exist.", username=username, code=code)

        session['username'] = username
        session['room'] = room_code
        return redirect(url_for('room', username=username, code=room_code))

    return render_template('index.html')


@app.route('/room/<string:username>/<string:code>')
def room(username, code):
    room_code = session.get('room')
    if room_code is None or session.get('username') is None:
        return redirect(url_for('index'))

    # Check if room exists in MongoDB
    room = mongo.db.rooms.find_one({"code": room_code})
    if not room:
        session.clear()
        return redirect(url_for('index'))

    # Get messages for this room
    messages = list(mongo.db.messages.find(
        {"room_code": room_code},
        {"_id": 0, "username": 1, "content": 1, "timestamp": 1}
    ).sort("timestamp", 1))

    # Format messages for template
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "username": msg["username"],
            "msg": msg["content"],
            "timestamp": msg["timestamp"].strftime("%I:%M:%p")
        })

    return render_template('room.html', username=username, code=code, messages=formatted_messages)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
