import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print("Server is running...")
print("Waiting for clients...")

clients = []
lock = threading.Lock()

def handle_client(client):
    username = ""

    try:
        username = client.recv(1024).decode().strip()

        if not username:
            return

        with lock:
            clients.append(client)
            count = len(clients)

        print(username, "joined the server!")
        print("Connected clients:", count)

        client.sendall(("Welcome " + username + "!\n").encode())

        while True:
            message = client.recv(1024).decode()

            if not message:
                break

            print(username + ": " + message)

            with lock:
                others = [c for c in clients if c != client]

            for other in others:
                try:
                    other.sendall((username + ": " + message + "\n").encode())
                except OSError:
                    pass

    except (ConnectionError, OSError):
        pass

    finally:
        with lock:
            if client in clients:
                clients.remove(client)
            count = len(clients)

        print(username or "A client", "disconnected.")
        print("Connected clients:", count)
        client.close()

while True:
    client, address = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client,),
        daemon=True
    )
    thread.start()