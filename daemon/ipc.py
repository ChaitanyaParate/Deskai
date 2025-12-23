import socket
import os
import threading

SOCKET_PATH = os.path.join(
    os.environ.get("XDG_RUNTIME_DIR", "/tmp"),
    "deskai.sock"
)

def start_ipc_server(on_command):
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)

    def loop():
        while True:
            conn, _ = server.accept()
            data = conn.recv(4096).decode().strip()
            if data:
                on_command(data)
            conn.close()

    threading.Thread(target=loop, daemon=True).start()
