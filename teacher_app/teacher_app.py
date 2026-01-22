import flet as ft
import requests
from teacher.connect import run_query
import random
import string
import asyncio

PRIMARY = "#6366F1"
BG = "#fafaf9"
CARD = "#ffffff"

def generate_code():
    return "".join(random.choices(string.digits, k=5))

def main(page: ft.Page):
    page.title = "Teacher Dashboard"
    page.window_width = 720
    page.window_height = 820
    page.bgcolor = BG
    page.padding = 20

    email = ft.TextField(
        label="Email",
        width=360,
        border_radius=12
    )
    error = ft.Text(color="red")

    session_id = None
    current_question_id = None
    answers_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO)

    # ---------------- LOGIN ----------------
    def login(e):
        rows = run_query(
            "SELECT id, name FROM teachers WHERE email=%s",
            [email.value],
            fetch=True
        )
        if rows:
            teacher_id, name = rows[0]
            show_dashboard(teacher_id, name)
        else:
            error.value = "Teacher not found"
            page.update()

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Teacher Login", size=26, weight="bold"),
                    email,
                    ft.ElevatedButton(
                        "Login",
                        bgcolor=PRIMARY,
                        color="black",
                        on_click=login
                    ),
                    error,
                ],
                spacing=16,
                horizontal_alignment="center",
            ),
            alignment=ft.Alignment(0,0),
            expand=True
        )
    )

    # ---------------- DASHBOARD ----------------
    def show_dashboard(teacher_id, teacher_name):
        nonlocal session_id, current_question_id
        page.clean()

        code = generate_code()
        session_id = run_query(
            """
            INSERT INTO sessions (teacher_id, code, is_active)
            VALUES (%s, %s, true)
            RETURNING id
            """,
            [teacher_id, code],
            fetch=True
        )[0][0]

        question_input = ft.TextField(
            hint_text="Type your question here...",
            multiline=True,
            min_lines=3,
            border_radius=12
        )

        # ---------- Actions ----------
        def start_question(e):
            nonlocal current_question_id
            q = run_query(
                """
                INSERT INTO questions (session_id, text, is_open)
                VALUES (%s, %s, true)
                RETURNING id
                """,
                [session_id, question_input.value],
                fetch=True
            )
            current_question_id = q[0][0]
            page.snack_bar = ft.SnackBar(ft.Text("Question started"))
            page.snack_bar.open = True
            page.update()

        def close_question(e):
            run_query(
                "UPDATE questions SET is_open=false WHERE id=%s",
                [current_question_id]
            )
            page.snack_bar = ft.SnackBar(ft.Text("Question closed"))
            page.snack_bar.open = True
            page.update()

        # ---------- Answers ----------
        def refresh_answers():
            if not current_question_id:
                return

            res = requests.get(
                f"http://127.0.0.1:8000/api/answers/{current_question_id}"
            ).json()

            answers_column.controls.clear()

            for a in res:
                answers_column.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(a["name"], weight="bold"),
                                        ft.Text(a["text"], size=14),
                                    ],
                                    expand=True
                                ),
                                ft.IconButton(
                                    icon="star" if a["starred"] else "star_border",
                                    icon_color=PRIMARY,
                                    on_click=lambda e, aid=a["id"]:
                                        requests.post(
                                            f"http://127.0.0.1:8000/api/star/{aid}"
                                        )
                                )
                            ]
                        ),
                        padding=14,
                        bgcolor=CARD,
                        border_radius=16,
                        shadow=ft.BoxShadow(
                                blur_radius=12,
                                color="#00000020"  # black with ~12% opacity
                            )

                    )
                )
            page.update()

        async def auto_refresh():
            while True:
                await asyncio.sleep(2)
                refresh_answers()

        page.run_task(auto_refresh)

        # ---------------- UI LAYOUT ----------------
        page.add(
            # Header
            ft.Row(
                [
                    ft.Text("🎓 Teacher Dashboard", size=24, weight="bold"),
                    ft.Container(expand=True),
                    ft.Text(teacher_name, weight="bold")
                ]
            ),

            # Session Card
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(f"Class Code: {code}", size=20, weight="bold"),
                        ft.IconButton(
                            icon="content_copy",
                            on_click=lambda e: page.set_clipboard(code)
                        )

                    ]
                ),
                padding=20,
                bgcolor=CARD,
                border_radius=16,
                shadow=ft.BoxShadow(
    blur_radius=12,
    color="#00000020"  # black with ~12% opacity
)

            ),

            # Question Card
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Ask a Question", size=18, weight="bold"),
                        question_input,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Start",
                                    bgcolor=PRIMARY,
                                    color="black",
                                    on_click=start_question
                                ),
                                ft.OutlinedButton(
                                    "Close",
                                    on_click=close_question
                                )
                            ]
                        )
                    ],
                    spacing=12
                ),
                padding=20,
                bgcolor=CARD,
                border_radius=16,
                shadow=ft.BoxShadow(
    blur_radius=12,
    color="#00000020"  # black with ~12% opacity
)

            ),

            ft.Text("Live Answers", size=20, weight="bold"),
            answers_column
        )

ft.app(target=main)
