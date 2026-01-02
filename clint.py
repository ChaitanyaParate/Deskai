import socket
import sys

SOCKET_PATH = "/tmp/deskai.sock"

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(SOCKET_PATH)

client.sendall(" ".join(sys.argv[1:]).encode())
print(client.recv(1024).decode())

client.close()
