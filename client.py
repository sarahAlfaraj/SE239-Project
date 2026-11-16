import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter your username: ")
client.sendall(username.encode())

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()

            if not message:
                break

            print("\n" + message)
        except (ConnectionError, OSError):
            break

thread = threading.Thread(
    target=receive_messages,
    daemon=True
)
thread.start()

print("Type messages or 'exit' to leave.")

while True:
    message = input()

    if message.lower() == "exit":
        break

    try:
        client.sendall(message.encode())
    except (ConnectionError, OSError):
        break

client.close()