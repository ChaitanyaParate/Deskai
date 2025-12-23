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
client.sendall(cmd.encode())
client.close()
