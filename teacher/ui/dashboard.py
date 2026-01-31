import flet as ft
import time

from teacher.ui.reviews_answers import review_answers_view
from teacher.ui.summary_view import summary_view

from ..config import CARD, DASHBOARD_BUTTON_STYLE, PRIMARY, BG
from .live_question import live_question_view
from ..utils import generate_code
from ..services.db import create_session, create_question, close_question


def dashboard_view(page, teacher_id, teacher_name, state):
    page.bgcolor = BG

    history_column = ft.Column(spacing=12)

    # -------- SESSION INIT --------
    if not state.session_id:
        code = generate_code()
        state.session_id = create_session(teacher_id, code)
        state.session_code = code
    else:
        code = state.session_code

    # -------- INPUT --------
    question_input = ft.TextField(
        hint_text="Type your question here...",
        multiline=True,
        min_lines=3,
        border_radius=12,
        filled=True,
        bgcolor="#f9fafb",
    )

    # -------- ACTIONS --------
    def start_question(e):
        if not question_input.value.strip():
            return

        state.current_question_id = create_question(
            state.session_id,
            question_input.value,
            timeout_seconds=timeout_seconds,
        )
        state.current_question_text = question_input.value
        state.question_start_ts = time.time()

        page.clean()
        page.add(
            live_question_view(
                page,
                state,
                on_close=close_current_question,
            )
        )
    def show_summary(question):
        page.clean()
        page.add(
            summary_view(
                page,
                question,
                on_back=lambda e: (
                    page.clean(),
                    page.add(
                        dashboard_view(
                            page,
                            teacher_id,
                            teacher_name,
                            state
                        )
                    )
                ),
                on_review=lambda q: (
                    page.clean(),
                    page.add(
                        review_answers_view(
                            page,
                            q,
                            on_back=lambda e: show_summary(q)
                        )
                    )
                )
            )
        )



    def close_current_question(e=None):
        elapsed = int(time.time() - state.question_start_ts)
        duration = f"{elapsed//60:02d}:{elapsed%60:02d}"

        close_question(state.current_question_id)

        state.closed_questions.insert(
                0,
                {
                    "id": state.current_question_id,   # 👈 THIS LINE
                    "text": state.current_question_text,
                    "duration": duration,
                }
            )


        state.current_question_id = None
        state.current_question_text = None
        state.question_start_ts = None

        page.clean()
        page.add(
            dashboard_view(
                page,
                teacher_id,
                teacher_name,
                state
            )
        )

    # -------- HISTORY --------
    def refresh_history():
        history_column.controls.clear()

        for q in state.closed_questions:
            history_column.controls.append(
                ft.Container(
                    padding=14,
                    bgcolor=CARD,
                    border_radius=12,
                    content=ft.Row(
                        [
                            ft.Text(q["text"], expand=True, weight="bold"),
                            ft.Text(q["duration"]),
                            ft.TextButton(
                                    "View Summary",
                                    on_click=lambda e, q=q: show_summary(q)
                                )

                        ]
                    ),
                )
            )

    refresh_history()

    # -------- MAIN CARD --------
    activity_card = ft.Container(
        padding=24,
        bgcolor=CARD,
        border_radius=20,
        content=ft.Column(
            [
                ft.Text("SHORT ANSWER ACTIVITY", size=12, weight="bold", color=PRIMARY),
                history_column,
                question_input,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Start Question",
                            bgcolor=PRIMARY,
                            color="white",
                            style=DASHBOARD_BUTTON_STYLE,
                            on_click=start_question,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=16,
        ),
    )

    # -------- FINAL LAYOUT --------
    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text(f"{teacher_name}'s ClassPoint", size=22, weight="bold"),
                    ft.Container(expand=True),
                    ft.Text("Live Session •", size=16, weight="bold"),
                    ft.Text(code, size=20, weight="bold", color=PRIMARY),
                ]
            ),
            activity_card,
        ],
        spacing=24,
    )
