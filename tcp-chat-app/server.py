
import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

clients = {}
clients_lock = threading.Lock()


def broadcast(message, sender=None):
    """Send a message to every connected client except the sender."""
    data = (message + "\n").encode("utf-8")

    with clients_lock:
        connected_clients = list(clients.keys())

    for client in connected_clients:
        if client == sender:
            continue

        try:
            client.sendall(data)
        except OSError:
            pass


def send_private_message(sender, recipient_name, message):
    """Send a private message to a specific user."""

    with clients_lock:
        sender_name = clients.get(sender, "Unknown")

        recipient = next(
            (
                client
                for client, name in clients.items()
                if name.lower() == recipient_name.lower()
            ),
            None
        )

    if recipient is None:
        sender.sendall(b"[SERVER] User not found.\n")
        return

    if recipient == sender:
        sender.sendall(
            b"[SERVER] You cannot send a private message to yourself.\n"
        )
        return

    timestamp = datetime.now().strftime("%H:%M:%S")

    response = (
        f"[PRIVATE {timestamp}] {sender_name}: {message}\n"
    )

    try:
        recipient.sendall(response.encode("utf-8"))
        sender.sendall(
            f"[SERVER] Private message sent to {recipient_name}.\n"
            .encode("utf-8")
        )
    except OSError:
        try:
            sender.sendall(
                b"[SERVER] Could not deliver the message.\n"
            )
        except OSError:
            pass


def handle_client(conn, address):
    username = None
    buffer = b""

    print(f"Connection established: {address}")

    try:
        while True:
            data = conn.recv(4096)

            if not data:
                break

            buffer += data

            # Process complete newline-terminated messages.
            while b"\n" in buffer:
                raw_message, buffer = buffer.split(b"\n", 1)
                message = raw_message.decode("utf-8").strip()

                if not message:
                    continue

                # First message is the username.
                if username is None:
                    username = message[:30]

                    with clients_lock:
                        clients[conn] = username

                    print(f"{username} joined from {address}")

                    broadcast(
                        f"[SERVER] {username} joined the chat."
                    )
                    continue

                # Quit command.
                if message.lower() == "/quit":
                    return

                # Private message command: /msg username message
                if message.startswith("/msg "):
                    parts = message.split(" ", 2)

                    if len(parts) < 3 or not parts[1] or not parts[2]:
                        conn.sendall(
                            b"[SERVER] Usage: /msg username message\n"
                        )
                    else:
                        send_private_message(
                            conn,
                            parts[1],
                            parts[2]
                        )

                    continue

                # Normal group message.
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_message = (
                    f"[{timestamp}] {username}: {message}"
                )

                print(formatted_message)
                broadcast(formatted_message, sender=conn)

    except (ConnectionResetError, OSError) as error:
        print(f"Connection lost: {address} ({error})")

    finally:
        with clients_lock:
            old_username = clients.pop(conn, None)

        try:
            conn.close()
        except OSError:
            pass

        if old_username:
            print(f"{old_username} disconnected.")
            broadcast(
                f"[SERVER] {old_username} left the chat."
            )


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    try:
        server.bind((HOST, PORT))
        server.listen()

        print(f"Chat server listening on port {PORT}")
        print("Waiting for clients...")

        while True:
            conn, address = server.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(conn, address),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\nServer shutting down.")

    except OSError as error:
        print(f"Server error: {error}")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()
