# A-simple-chat-app
# Simple Chat Application

This is a simple, real-time chat application built using Flask, Socket.IO, and MongoDB. Users can create chat rooms, join existing rooms, and send messages to each other in real-time.

## Features

*   **Real-time Chat:** Messages are sent and received instantly using Socket.IO.
*   **Create Rooms:** Users can create new chat rooms with unique codes.
*   **Join Rooms:** Users can join existing chat rooms by entering the room code.
*   **Persistent Messages:** Messages are stored in a MongoDB database, so they persist even if users disconnect and reconnect.
*   **User Join/Leave Messages:** The chat displays messages when users join or leave the room.
*   **Username Display:** Each message is displayed with the username of the sender.
*   **Timestamp:** Each message has a timestamp.
* **Refresh**: When the user refresh the page, the messages are still there.
* **MongoDB**: The messages and the rooms are stored in a MongoDB database.

## Technologies Used

*   **Flask:** A lightweight Python web framework.
*   **Socket.IO:** A library for real-time, bidirectional communication.
*   **MongoDB:** A NoSQL database for storing messages and room data.
*   **PyMongo:** The official Python driver for MongoDB.
*   **Flask-PyMongo:** A Flask extension for working with PyMongo.
*   **Python-dotenv:** To manage environment variables.
*   **HTML, CSS, JavaScript:** For the frontend user interface.

## Project Structure
## Setup and Installation

1.  **Clone the Repository:**
2.  **Install Dependencies:**
3.  **Set Up Environment Variables:**

    *   Create a `.env` file in the root directory of the project.
    *   Add the following variables to the `.env` file:
    *   **`SECRET_KEY`:** This is used for Flask's session management. Generate a strong, random key.
    *   **`MONGO_URI`:** This is your MongoDB connection string. If you're running MongoDB locally, the default value is usually fine. If you're using a cloud-hosted MongoDB, replace this with your connection string.

4.  **Start MongoDB:**

    *   Make sure you have MongoDB installed and running.
    *   If you're running it locally, you can usually start it with:
5.  **Run the Application:**
    *   This will start the Flask development server. You should see output indicating that the server is running.

6.  **Open in Browser:**

    *   Open your web browser and go to `http://127.0.0.1:5000/`.

## How to Use

1.  **Create a Room:**
    *   Enter a username in the "Name" field.
    *   Click the "Create a room" button.
    *   You will be redirected to the chat room, and a unique room code will be generated.

2.  **Join a Room:**
    *   Enter a username in the "Name" field.
    *   Enter the room code in the "Room code" field.
    *   Click the "Join a room" button.
    *   You will be redirected to the chat room.

3.  **Send Messages:**
    *   Type your message in the input field at the bottom of the chat room.
    *   Click the "Send" button or press Enter.
    *   Your message will appear in the chat, along with your username and a timestamp.

4. **Refresh the page**:
    * When you refresh the page, the messages will still be there.

## Future Improvements

*   **User Authentication:** Add user login/registration to track users more effectively.
*   **Private Messaging:** Allow users to send private messages to each other.
*   **Message Editing/Deletion:** Allow users to edit or delete their own messages.
*   **Room Management:** Add features for room owners to manage their rooms (e.g., kicking users, setting room topics).
*   **Improved UI/UX:** Enhance the user interface and user experience.
* **Deployment**: Deploy the application to a server.

## Contributing

If you'd like to contribute to this project, please feel free to fork the repository and submit a pull request.

## License

[Choose a license, e.g., MIT License]