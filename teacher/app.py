from ensurepip import bootstrap
import flet as ft
import socket
import sys
import threading
from urllib.parse import parse_qs, urlparse
from teacher.config import BG
from teacher.state import AppState
from teacher.ui.login import login_view
from teacher.ui.dashboard import dashboard_view
from teacher.ui.setup import setup_view
from teacher.ui.live_question import live_question_view
from teacher.bootsrap_db import bootstrap_tables

bootstrap_tables()

PROTOCOL_SCHEME = "shortanswer"
SINGLE_INSTANCE_PORT = 56789
BUFFER_SIZE = 4096


def extract_protocol_url(argv):
    for arg in argv[1:]:
        if arg.startswith(f"{PROTOCOL_SCHEME}://"):
            return arg
    return None


def send_protocol_url(url):
    try:
        with socket.create_connection(("127.0.0.1", SINGLE_INSTANCE_PORT), timeout=1) as client:
            client.sendall(url.encode("utf-8"))
        return True
    except OSError:
        return False


def ensure_single_instance(protocol_url):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(("127.0.0.1", SINGLE_INSTANCE_PORT))
        server_socket.listen()
        return server_socket
    except OSError:
        if protocol_url:
            send_protocol_url(protocol_url)
        else:
            send_protocol_url(f"{PROTOCOL_SCHEME}://open")
        return None


INITIAL_PROTOCOL_URL = extract_protocol_url(sys.argv)
SERVER_SOCKET = ensure_single_instance(INITIAL_PROTOCOL_URL)
if SERVER_SOCKET is None:
    raise SystemExit(0)
def main(page: ft.Page):
    page.title = "Teacher Dashboard"
    page.bgcolor = BG
    page.padding = 20

    state = AppState()

    # ---------- NAVIGATION (OLD-FLET SAFE) ----------

    def show_login():
        page.clean()
        page.add(
            login_view(page, on_login_success)
        )

    def show_setup(teacher_id, teacher_name):
        page.clean()
        page.add(
            setup_view(
                page,
                state,
                on_start=lambda: show_dashboard(teacher_id, teacher_name)
            )
        )

    def show_dashboard(teacher_id, teacher_name):
        page.clean()
        page.add(
            dashboard_view(
                page,
                teacher_id,
                teacher_name,
                state
            )
        )

    def show_live():
        page.clean()
        page.add(
            live_question_view(
                page,
                state,
                on_close=show_dashboard_callback
            )
        )

    def show_dashboard_callback(e=None):
        show_dashboard(state.teacher_id, state.teacher_name)
    from ensurepip import bootstrap
import socket
import sys
import threading
from urllib.parse import parse_qs, urlparse
import flet as ft
from teacher.config import BG
from teacher.state import AppState
from teacher.ui.login import login_view
from teacher.ui.dashboard import dashboard_view
from teacher.ui.setup import setup_view
from teacher.ui.live_question import live_question_view
from teacher.bootsrap_db import bootstrap_tables

bootstrap_tables()

PROTOCOL_SCHEME = "shortanswer"
SINGLE_INSTANCE_PORT = 56789
BUFFER_SIZE = 4096


def extract_protocol_url(argv):
    for arg in argv[1:]:
        if arg.startswith(f"{PROTOCOL_SCHEME}://"):
            return arg
    return None


def send_protocol_url(url):
    try:
        with socket.create_connection(("127.0.0.1", SINGLE_INSTANCE_PORT), timeout=1) as client:
            client.sendall(url.encode("utf-8"))
        return True
    except OSError:
        return False


def ensure_single_instance(protocol_url):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind(("127.0.0.1", SINGLE_INSTANCE_PORT))
        server_socket.listen()
        return server_socket
    except OSError:
        if protocol_url:
            send_protocol_url(protocol_url)
        else:
            send_protocol_url(f"{PROTOCOL_SCHEME}://open")
        return None


INITIAL_PROTOCOL_URL = extract_protocol_url(sys.argv)
SERVER_SOCKET = ensure_single_instance(INITIAL_PROTOCOL_URL)
if SERVER_SOCKET is None:
    raise SystemExit(0)


def main(page: ft.Page):
    page.title = "Teacher Dashboard"
    page.bgcolor = BG
    page.padding = 20

    state = AppState()

    # ---------- NAVIGATION (OLD-FLET SAFE) ----------

    def show_login():
        page.clean()
        page.add(
            login_view(page, on_login_success)
        )

    def show_setup(teacher_id, teacher_name):
        page.clean()
        page.add(
            setup_view(
                page,
                state,
                on_start=lambda: show_dashboard(teacher_id, teacher_name)
            )
        )

    def show_dashboard(teacher_id, teacher_name):
        page.clean()
        page.add(
            dashboard_view(
                page,
                teacher_id,
                teacher_name,
                state
            )
        )

    def show_live():
        page.clean()
        page.add(
            live_question_view(
                page,
                state,
                on_close=show_dashboard_callback
            )
        )

    def show_dashboard_callback(e=None):
        show_dashboard(state.teacher_id, state.teacher_name)

    def handle_protocol_url(url):
        parsed = urlparse(url)
        route = parsed.netloc or parsed.path.lstrip("/")
        params = parse_qs(parsed.query)

        if hasattr(page, "window_to_front"):
            page.window_to_front()

        if route in ("login", "open", ""):
            show_login()
            return

        if route == "start-session":
            state.pending_session = params
            show_login()
            return

        show_login()

    def start_protocol_listener():
        def listen_loop():
            while True:
                conn, _ = SERVER_SOCKET.accept()
                data = conn.recv(BUFFER_SIZE)
                conn.close()
                if data:
                    url = data.decode("utf-8").strip()
                    if url:
                        page.call_from_thread(lambda: handle_protocol_url(url))

        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()
    # ---------- LOGIN SUCCESS ----------

    def on_login_success(teacher_id, teacher_name):
        # store for back navigation
        state.teacher_id = teacher_id
        state.teacher_name = teacher_name
        show_setup(teacher_id, teacher_name)

    # ---------- INITIAL VIEW ----------
    show_login()
    start_protocol_listener()
    if INITIAL_PROTOCOL_URL:
        handle_protocol_url(INITIAL_PROTOCOL_URL)
    #show_setup(teacher_id=1, teacher_name="Demo Teacher")

ft.app(target=main)
