import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from daemon.loop import run_daemon

if __name__ == "__main__":
    run_daemon()
