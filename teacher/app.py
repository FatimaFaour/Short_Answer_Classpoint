import flet as ft
from teacher.config import BG
from teacher.state import AppState
from teacher.ui.login import login_view
from teacher.ui.dashboard import dashboard_view
from teacher.ui.setup import setup_view
from teacher.ui.live_question import live_question_view

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

    # ---------- LOGIN SUCCESS ----------

    def on_login_success(teacher_id, teacher_name):
        # store for back navigation
        state.teacher_id = teacher_id
        state.teacher_name = teacher_name
        show_setup(teacher_id, teacher_name)

    # ---------- INITIAL VIEW ----------
    show_login()

ft.app(target=main)
