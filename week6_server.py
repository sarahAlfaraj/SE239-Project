import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 5000))
server.listen(1)

print("Server is running...")
print("Waiting for a client...")

client, address = server.accept()

print("Client connected!")

message = client.recv(1024).decode()
print("Client says:", message)

client.sendall("Hello from server!".encode())

client.close()
server.close()