import flet as ft
import requests
from connect import run_query
import random
import string
import asyncio

def generate_code():
    return "".join(random.choices(string.digits, k=5))

def main(page: ft.Page):
    page.title = "Teacher Dashboard"
    page.window_width = 600
    page.window_height = 750

    email = ft.TextField(label="Email", width=350)
    error = ft.Text(color="red")

    session_id = None
    current_question_id = None
    answers_column = ft.Column(scroll=ft.ScrollMode.AUTO)


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
        ft.Text("Teacher Login", size=22, weight="bold"),
        email,
        ft.ElevatedButton("Login", on_click=login),
        error
    )

    def show_dashboard(teacher_id, teacher_name):
        nonlocal current_question_id
        page.clean()

        code = generate_code()
        nonlocal session_id

        result = run_query(
            """
            INSERT INTO sessions (teacher_id, code)
            VALUES (%s, %s)
            RETURNING id
            """,
            [teacher_id, code],
            fetch=True
        )

        session_id = result[0][0]


        question_input = ft.TextField(label="Question", multiline=True, width=450)

        def start_question(e):
            nonlocal current_question_id
            q = run_query(
                """
                INSERT INTO questions (session_id, text, is_open)
                VALUES (
                    (SELECT id FROM sessions WHERE code=%s AND is_active=true),
                    %s,
                    true
                )
                RETURNING id
                """,
                [code, question_input.value],
                fetch=True
            )

            current_question_id = q[0][0]

            page.snack_bar = ft.SnackBar(ft.Text("Question started"))
            page.snack_bar.open = True
            page.update()

        def close_question(e):
            run_query(
                """
                UPDATE questions
                SET is_open=false
                WHERE id=%s
                """,
                [current_question_id]
            )

            page.snack_bar = ft.SnackBar(ft.Text("Question closed"))
            page.snack_bar.open = True
            page.update()

        def refresh_answers():
            nonlocal current_question_id, session_id

            if not session_id:
                return

            # If question not known yet, fetch it
            if not current_question_id:
                q = requests.get(
                    f"http://127.0.0.1:8000/api/question/{session_id}"
                ).json()

                if not q or not q.get("id"):
                    return

                current_question_id = q["id"]

            res = requests.get(
                f"http://127.0.0.1:8000/api/answers/{current_question_id}"
            )

            answers_column.controls.clear()

            for a in res.json():
                answers_column.controls.append(
                    ft.Text(f"{a['name']}: {a['text']}")
                )

            page.update()



        # auto refresh every 2 seconds
        async def auto_refresh():
            while True:
                await asyncio.sleep(2)
                refresh_answers()

        page.run_task(auto_refresh)



        page.add(
            ft.Text(f"Welcome {teacher_name}", size=22, weight="bold"),
            ft.Text(f"Session Code: {code}", size=18),
            question_input,
            ft.ElevatedButton("Start Question", on_click=start_question),
            ft.ElevatedButton("Close Question", on_click=close_question),
            ft.Divider(),
            ft.Text("Live Answers", size=20, weight="bold"),
            answers_column
        )

ft.app(target=main)
