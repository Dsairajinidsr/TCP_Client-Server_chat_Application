
import socket
import threading

HOST = input("Enter server IP (127.0.0.1 for this laptop): ").strip()
PORT = 5000


def receive_messages(client):
    """Receive incoming chat messages in the background."""
    buffer = b""

    try:
        while True:
            data = client.recv(4096)

            if not data:
                print("\nServer disconnected.")
                break

            buffer += data

            while b"\n" in buffer:
                raw_message, buffer = buffer.split(b"\n", 1)
                message = raw_message.decode("utf-8")
                print(f"\n{message}")

    except OSError:
        pass

    finally:
        print("\nReceive connection closed.")


def start_client():
    username = input("Enter your username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        client.sendall((username[:30] + "\n").encode("utf-8"))

        print("Connected to the chat server!")
        print("Type a message and press Enter.")
        print("Type /quit to leave the chat.\n")

        receiver = threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True
        )
        receiver.start()

        while True:
            message = input()

            if not message.strip():
                continue

            client.sendall((message + "\n").encode("utf-8"))

            if message.strip().lower() == "/quit":
                break

    except ConnectionRefusedError:
        print("Cannot connect. Make sure the server is running.")

    except (OSError, KeyboardInterrupt):
        print("\nDisconnected from the chat.")

    finally:
        client.close()


if __name__ == "__main__":
    start_client()
