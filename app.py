import flet as ft
import psycopg2

# --- Database connection ---
def get_connection():
    return psycopg2.connect(
        host="192.168.56.1",
        database="short_ans_classpoint",
        user="postgres",
        password="ahmad1807",
        port="5432",
        
    )

# --- Insert a question ---
def add_question(question):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO questions (text) VALUES (%s);", (question,))
    conn.commit()
    cur.close()
    conn.close()

# --- Retrieve all questions ---
def get_questions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM questions ORDER BY id DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# --- Flet UI ---
def main(page: ft.Page):
    page.title = "Teacher Dashboard"
    page.scroll = "adaptive"

    question_input = ft.TextField(label="Enter a question", width=400)
    questions_list = ft.Column()

    def refresh_questions():
        questions_list.controls.clear()
        for q in get_questions():
            questions_list.controls.append(ft.Text(f"{q[1]}", size=16))
        page.update()

    def on_submit(e):
        if question_input.value.strip():
            add_question(question_input.value)
            question_input.value = ""
            refresh_questions()

    submit_btn = ft.ElevatedButton("Add Question", on_click=on_submit)

    page.add(
        ft.Text("Teacher's Dashboard", size=24, weight="bold"),
        question_input,
        submit_btn,
        ft.Divider(),
        ft.Text("All Questions:", size=20),
        questions_list
    )

    refresh_questions()

ft.app(target=main)
