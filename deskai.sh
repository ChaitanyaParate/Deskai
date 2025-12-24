#!/usr/bin/env python3
import sys
import socket

SOCKET_PATH = "/tmp/deskai.sock"

if "--task" not in sys.argv:
    print("Usage: deskai --task \"command\"")
    sys.exit(1)

cmd = sys.argv[sys.argv.index("--task") + 1]

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(SOCKET_PATH)
# client.sendall(cmd.encode())
# response = client.recv(65536)
# print(response.decode())
# client.close()

client.sendall(cmd.encode())
client.settimeout(None)

while True:
    chunk = client.recv(4096)
    if not chunk:
        break
    print(chunk.decode(), end="", flush=True)

client.close()

