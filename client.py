import socket
import sys

SOCKET_PATH = "/tmp/deskai.sock"
# ---- Clint Command Execution ----
def stream(task):
    
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    message = f"stream {task}".encode('utf-8')
    
    client.sendall(message)

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
    try:
        if len(sys.argv) < 2:
            print("usage: deskai <command>", flush=True)
            sys.exit(1)

        if sys.argv[1] == "stream":
            if len(sys.argv) < 3:
                print("usage: deskai stream <task>", flush=True)
                sys.exit(1)

            stream(sys.argv[2])



        else:
            send(" ".join(sys.argv[1:]))
    except KeyboardInterrupt:
        print("deskai Exited", flush=True)
        sys.exit(1)


