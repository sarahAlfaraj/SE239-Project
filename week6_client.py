import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 5000))

print("Connected to server!")

message = input("Enter a message: ")
client.sendall(message.encode())

reply = client.recv(1024).decode()
print("Server says:", reply)

client.close()