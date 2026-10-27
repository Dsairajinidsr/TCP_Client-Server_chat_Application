# TCP Client–Server Chat Application

## 1. Project Overview

The TCP Client–Server Chat Application is a real-time messaging system developed using Python socket programming. It allows multiple clients to communicate through a central server using TCP connections.

## 2. Objectives

- Establish communication using TCP sockets.
- Implement client–server architecture.
- Support multiple clients using threading.
- Broadcast messages to connected users.
- Support private messaging and timestamps.
- Handle client disconnections.

## 3. Technologies Used

- Python 3
- TCP/IP
- Socket Programming
- Multithreading
- VS Code
- Windows Terminal or Linux CLI

## 4. Project Structure

```text
tcp-chat-app/
├── server.py
├── client.py
└── README.md
```

## 5. Requirements

- Python 3 installed
- A code editor or terminal
- No external Python packages required

## 6. How to Run the Project

### Step 1: Open the project directory

Open a terminal in the `tcp-chat-app` folder.

### Step 2: Start the server

```bash
python server.py
```

### Step 3: Start a client

Open another terminal and run:

```bash
python client.py
```

Enter `127.0.0.1` as the server IP when testing on the same computer.

### Step 4: Connect additional clients

Open more terminals and run `python client.py` in each terminal.

### Step 5: Send messages

Type a message and press Enter to broadcast it to other connected clients.

For private messaging, use:

```text
/msg Student2 Hello
```

To disconnect, type:

```text
/quit
```

## 7. Main Features

- Multiple client connections
- Real-time message broadcasting
- Private messaging
- Timestamps
- Thread-based client handling
- Connection and disconnection notifications

## 8. Conclusion

This project demonstrates practical concepts in computer networking, TCP communication, socket programming, and multithreading. It provides a foundation for developing more advanced messaging applications.

## 9. Future Enhancements

- Graphical user interface
- User authentication
- Persistent chat history
- File sharing
- Encrypted communication using TLS
