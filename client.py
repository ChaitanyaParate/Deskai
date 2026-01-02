import socket
import sys

SOCKET_PATH = "/tmp/deskai.sock"

def stream():
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    client.sendall(b"stream")

    while True:
        data = client.recv(1024)
        if not data:
            break
        print(data.decode(), end="", flush=True)

    client.close()


def send(cmd):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    client.sendall(cmd.encode())
    resp = client.recv(65536).decode()
    client.close()
    print(resp)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: deskai <command>")
        sys.exit(1)

    if sys.argv[1] == "stream":
        stream()
    else:
        send(" ".join(sys.argv[1:]))



# import socket
# import sys

# SOCKET_PATH = "/tmp/deskai.sock"

# client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# client.connect(SOCKET_PATH)

# client.sendall(" ".join(sys.argv[1:]).encode())
# print(client.recv(1024).decode())

# client.close()
