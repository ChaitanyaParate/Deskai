import socket
import os
import threading
import sys

import subprocess
import time

from daemon.loop import run_daemon
from state import shared_data
from intent.router.router import route_intent
from intent.executo.executor import execute_intent

SOCKET_PATH = "/tmp/deskai.sock"


def socket_server():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)

    print("[deskai] socket server running", flush=True)

    while True:
        try:
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
            
            elif command.split(' ')[0] == "stream":

                with shared_data.lock:
                    intent = route_intent(command.split(' ')[1], shared_data.context)
                    text = [shared_data.text, shared_data.context]

                if not text:
                    conn.sendall(b"No text available\n")
                    conn.close()
                    return
                if intent == "Noop":
                    conn.sendall(b"\n[deskai] Incorrect Command\n")
                    sys.exit(1)
                try:
                    conn.sendall(b"[deskai] streaming started\n")
                    for chunk in execute_intent(intent, {"text": text}):
                        conn.sendall(chunk.encode())

                    conn.sendall(b"\n[deskai] streaming complete\n")
                except BrokenPipeError:
                    print("[deskai] client disconnected, stopping stream")
                    conn.close()

                conn.close()
        except KeyboardInterrupt:
            
            print("[deskai] Exit")
            sys.exit(1)
            
def start_ollama():
    log = open("/tmp/ollama.log", "ab", buffering=0)

    subprocess.Popen(
        ["ollama", "serve"],
        stdout=log,
        stderr=log,
        stdin=subprocess.DEVNULL,
        start_new_session=True
    )

def ollama_running():
    return subprocess.run(
        ["pgrep", "-f", "ollama serve"],
        stdout=subprocess.DEVNULL
    ).returncode == 0

def main():
    
    threading.Thread(target=run_daemon, daemon=True).start()
    time.sleep(1)

    if not ollama_running():
        start_ollama()
    
    socket_server()






if __name__ == "__main__":
    main()
