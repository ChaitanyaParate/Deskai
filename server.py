import socket
import os
from state import shared_data

SOCKET_PATH = "/tmp/shared_writer.sock"

if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(5)

print("Server running. Waiting for commands...")

while True:
    conn, _ = server.accept()
    command = conn.recv(1024).decode().strip()

    if command == "exit":
        conn.sendall(b"Server shutting down\n")
        conn.close()
        break

    try:
        value = int(command)
        with shared_data.lock:
            shared_data.value = value
        conn.sendall(f"Value updated to {value}\n".encode())
    except ValueError:
        conn.sendall(b"Invalid command. Send an integer.\n")

    conn.close()

server.close()
os.remove(SOCKET_PATH)
