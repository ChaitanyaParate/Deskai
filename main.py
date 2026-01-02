from daemon.loop import run_daemon
from daemon.state import GlobalState
from daemon.server import create_app
import threading
import uvicorn

def main():
    state = GlobalState()

    t = threading.Thread(target=run_daemon, args=(state,), daemon=True)
    t.start()

    app = create_app(state)
    uvicorn.run(app, host="127.0.0.1", port=7331)

if __name__ == "__main__":
    main()
