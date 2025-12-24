import socket
import os
import threading

SOCKET_PATH = "/tmp/deskai.sock"
_server_socket = None

def start_ipc_server(handle_command):
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(60)
    print("[deskai] IPC server listening", flush=True)

    def loop():
        while True:
            try:
                conn, _ = server.accept()
            except Exception as e:
                print("[deskai IPC] accept failed:", e, flush=True)
                continue

            try:
                data = conn.recv(4096)
                if not data:
                    conn.close()
                    continue

                cmd = data.decode().strip()
                result = handle_command(cmd)

                if isinstance(result, str):
                    conn.sendall(result.encode())
                elif result is None:
                    conn.sendall(b"[deskai] No output")
                else:
                    for chunk in result:
                        conn.sendall(chunk.encode())

            except BrokenPipeError:
                print("[deskai IPC] client disconnected early", flush=True)
            except Exception as e:
                print("[deskai IPC] handler error:", e, flush=True)
                try:
                    conn.sendall(f"[deskai ERROR] {e}".encode())
                except:
                    pass
            finally:
                conn.close()


    threading.Thread(target=loop, daemon=True).start()
