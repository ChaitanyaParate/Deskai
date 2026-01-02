import socket
import os
import threading

from daemon.loop import run_daemon
from daemon.llm_loop import llm_loop
from llm.warmup import warmup_llm
from state import shared_data
from intent.executo.handlers.explain_error import handle_explain_error

SOCKET_PATH = "/tmp/deskai.sock"


def socket_server():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)

    print("[deskai] socket server running")

    while True:
        conn, _ = server.accept()
        command = conn.recv(1024).decode().strip()

        if command == "exit":
            conn.sendall(b"shutting down\n")
            conn.close()
            os._exit(0)

        elif command == "read":
            with shared_data.lock:
                value = shared_data.value
                context = shared_data.context.label if shared_data.context else None
            conn.sendall(f"value={value}, context={context}\n".encode())

        elif command == "stream":
            conn.sendall(b"[deskai] streaming started\n")

            with shared_data.lock:
                text = shared_data.text

            if not text:
                conn.sendall(b"No text available\n")
                conn.close()
                return

            try:
                for chunk in handle_explain_error({"text": text}):
                    conn.sendall(chunk.encode())
                conn.sendall(b"\n[deskai] streaming complete\n")
            except Exception as e:
                conn.sendall(f"\n[deskai] error: {e}\n".encode())

            conn.close()


def main():
    #warmup_llm()
    threading.Thread(target=run_daemon, daemon=True).start()
    threading.Thread(target=llm_loop, daemon=True).start()
    socket_server()


if __name__ == "__main__":
    main()
