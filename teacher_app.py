import flet as ft
import psycopg2
import random

# --- Database Connection ---
def get_connection():
    return psycopg2.connect(
        host="192.168.56.1",
        database="short_ans_classpoint",
        user="postgres",
        password="ahmad1807",
        port="5432",
    )

# --- Helper: Generate 5-digit numeric session code ---
def generate_code():
    return str(random.randint(10000, 99999))

# --- Database Functions ---
def create_session(teacher_id, code):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sessions (teacher_id, code) VALUES (%s, %s) RETURNING id;",
        (teacher_id, code),
    )
    session_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return session_id

def add_question(session_id, text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO questions (session_id, text) VALUES (%s, %s);",
        (session_id, text),
    )
    conn.commit()
    cur.close()
    conn.close()

def get_questions(session_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, text FROM questions WHERE session_id=%s ORDER BY created_at DESC;",
        (session_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# --- PAGE 2: Session Page (with 'Collecting responses...' view) ---
def session_page(page: ft.Page, session_id, session_code):
    page.clean()
    page.title = f"Session {session_code} - Manage Questions"
    page.scroll = "adaptive"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # UI elements
    question_input = ft.TextField(label="Type a question to ask students", width=400)
    collecting_view = ft.Column(visible=False)
    normal_view = ft.Column()
    questions_list = ft.Column()

    # ============ inner helpers ============
    def refresh_questions():
        questions_list.controls.clear()
        for _, text in get_questions(session_id):
            questions_list.controls.append(ft.Text(f"• {text}", size=16))
        page.update()

    def show_collecting_view(question_text):
        """Show 'Collecting responses...' screen."""
        normal_view.visible = False
        collecting_view.visible = True
        collecting_view.controls.clear()
        collecting_view.controls.extend([
            ft.Text(f"Class code: {session_code}", size=26, weight="bold", color="blue"),
            ft.Text(f"Question: {question_text}", size=20, italic=True),
            ft.ProgressRing(),
            ft.Text("Collecting responses...", size=18, color="gray"),
            ft.Divider(),
            ft.Text("No participants yet. Waiting for students to join...", color="gray"),
            ft.ElevatedButton(
    "Close submission",
    bgcolor="#EF5350",   # same red as RED_400
    color="white",
    on_click=lambda e: close_submission()
)

        ])
        page.update()

    def close_submission():
        collecting_view.visible = False
        normal_view.visible = True
        refresh_questions()

    # ============ actions ============
    def ask_question(e):
        text = question_input.value.strip()
        if text:
            add_question(session_id, text)
            question_input.value = ""
            show_collecting_view(text)

    def go_back(e):
        page.clean()
        main_page(page)

    # ============ layout ============
    normal_view.controls.extend([
        ft.Text(f"🧑‍🏫 Session Code: {session_code}", size=22, weight="bold"),
        question_input,
        ft.ElevatedButton("Ask Question", on_click=ask_question),
        ft.Divider(),
        ft.Text("Previous Questions", size=20),
        questions_list,
        ft.Divider(),
        ft.ElevatedButton("⬅️ Back to Dashboard", on_click=go_back),
    ])

    page.add(normal_view, collecting_view)
    refresh_questions()


# --- PAGE 1: Main Dashboard ---
def main_page(page: ft.Page):
    page.title = "Teacher Dashboard - ClassPoint Prototype"
    page.window_width = 500
    page.window_height = 400
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    teacher_id = 1
    session_code_display = ft.Text("", size=26, weight="bold", color="green")

    def start_session(e):
        code = generate_code()
        session_id = create_session(teacher_id, code)
        session_code_display.value = f"Session Code: {code}"
        page.update()

        # ✅ Navigate to Session Page (same app, new page)
        session_page(page, session_id, code)

    page.add(
        ft.Text("📘 Teacher Dashboard", size=30, weight="bold"),
        ft.ElevatedButton("Start New Session", on_click=start_session),
        session_code_display,
    )


# --- APP ENTRY ---
def main(page: ft.Page):
    main_page(page)


ft.app(target=main, view=ft.AppView.FLET_APP)
