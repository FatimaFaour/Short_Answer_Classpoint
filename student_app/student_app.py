import flet as ft
from connect import run_query

def main(page: ft.Page):
    page.title = "Student Join"
    page.window_width = 450
    page.window_height = 600

    code = ft.TextField(label="Session Code", width=300)
    nickname = ft.TextField(label="Nickname", width=300)
    error = ft.Text(color="red")

    def join(e):
        session = run_query(
            "SELECT id FROM sessions WHERE code=%s AND is_active=true",
            [code.value],
            fetch=True
        )

        if not session:
            error.value = "Invalid session code"
            page.update()
            return

        session_id = session[0][0]

        run_query(
            "INSERT INTO students (display_name) VALUES (%s)",
            [nickname.value]
        )

        student_id = run_query(
            "SELECT id FROM students ORDER BY id DESC LIMIT 1",
            fetch=True
        )[0][0]

        run_query(
            """
            INSERT INTO participants (session_id, student_id, nickname)
            VALUES (%s, %s, %s)
            """,
            [session_id, student_id, nickname.value]
        )

        show_question(session_id, student_id)

    page.add(
        ft.Text("Join Session", size=22, weight="bold"),
        code,
        nickname,
        ft.ElevatedButton("Join", on_click=join),
        error
    )

    def show_question(session_id, student_id):
        page.clean()

        q = run_query(
            """
            SELECT id, text FROM questions
            WHERE session_id=%s AND is_open=true
            """,
            [session_id],
            fetch=True
        )

        if not q:
            page.add(ft.Text("Waiting for teacher question..."))
            return

        question_id, text = q[0]
        answer = ft.TextField(label="Your Answer", multiline=True, width=400)

        def submit(e):
            run_query(
                """
                INSERT INTO answer (question_id, student_id, answer_text)
                VALUES (%s, %s, %s)
                """,
                [question_id, student_id, answer.value]
            )
            page.snack_bar = ft.SnackBar(ft.Text("Answer submitted"))
            page.snack_bar.open = True
            page.update()

        page.add(
            ft.Text(text, size=20, weight="bold"),
            answer,
            ft.ElevatedButton("Submit Answer", on_click=submit)
        )

ft.app(target=main)
