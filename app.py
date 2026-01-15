import flet as ft
from teacher_app.connect import run_query

def main(page: ft.Page):
    page.title = "Student - Short Answer"
    page.window_width = 450
    page.window_height = 600

    # ---------- JOIN CLASS ----------
    class_code = ft.TextField(label="Class Code", width=300)
    student_name = ft.TextField(label="Your Name", width=300)
    error = ft.Text(color="red")

    def join_class(e):
        rows = run_query(
            "SELECT id FROM session WHERE class_code=%s",
            [class_code.value],
            fetch=True
        )
        if not rows:
            error.value = "Invalid class code"
            page.update()
            return

        run_query(
            "INSERT INTO student (display_name) VALUES (%s) RETURNING id",
            [student_name.value]
        )

        student_id = run_query(
            "SELECT id FROM student ORDER BY id DESC LIMIT 1",
            fetch=True
        )[0][0]

        show_question(student_id)

    page.add(
        ft.Text("Join Class", size=22, weight="bold"),
        class_code,
        student_name,
        ft.ElevatedButton("Join", on_click=join_class),
        error
    )

    # ---------- QUESTION VIEW ----------
    def show_question(student_id):
        page.clean()

        q = run_query("SELECT id, prompt FROM active_question", fetch=True)
        if not q:
            page.add(ft.Text("No active question"))
            return

        question_id, prompt = q[0]
        answer = ft.TextField(label="Your Answer", multiline=True, width=400)

        def submit_answer(e):
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
            ft.Text(prompt, size=20, weight="bold"),
            answer,
            ft.ElevatedButton("Submit Answer", on_click=submit_answer)
        )

ft.app(target=main)
