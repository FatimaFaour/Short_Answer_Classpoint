import threading
import flet as ft
import uvicorn

from backend.main import app as fastapi_app
from teacher.app import main as flet_main


def run_fastapi():
    config = uvicorn.Config(
        fastapi_app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        lifespan="on",
        reload=False,
        access_log=False,
    )
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    # شغّل FastAPI بالخلفية
    threading.Thread(target=run_fastapi, daemon=True).start()

    # شغّل Flet UI
    ft.app(target=flet_main)
