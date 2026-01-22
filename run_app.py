import subprocess
import sys
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def start_fastapi():
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
        ],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def start_flet():
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "teacher.app",
        ],
        cwd=BASE_DIR,
    )

if __name__ == "__main__":
    api = start_fastapi()
    time.sleep(2)  # wait for backend
    ui = start_flet()

    ui.wait()
    api.terminate()
