import flet as ft
from connect import run_query   # your database helper file


def main(page: ft.Page):
    page.title = "Short Answer ClassPoint - Teacher"
    page.window_width = 500
    page.window_height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # ========== SHARED VIEW SWITCHING ==========
    def show_login():
        page.clean()
        page.add(login_view)

    def show_signup():
        page.clean()
        page.add(signup_view)

    # ========== LOGIN VIEW ==========
    email = ft.TextField(label="Email", width=350)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=350)
    login_error = ft.Text("", color="#FF0000")

    def login_clicked(e):
        rows = run_query(
            "SELECT display_name FROM teacher WHERE email=%s AND password_hash=%s",
            [email.value, password.value],
            fetch=True,
        )
        if rows:
            teacher_name = rows[0][0]
            show_dashboard(teacher_name)
        else:
            login_error.value = "Invalid email or password"
            page.update()

    login_button = ft.ElevatedButton("Sign in", on_click=login_clicked)
    signup_link = ft.TextButton("Create a new account", on_click=lambda e: show_signup())

    login_view = ft.Column(
        [
            ft.Text("Teacher Login", size=22, weight="bold"),
            email,
            password,
            login_button,
            signup_link,
            login_error,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ========== SIGN-UP VIEW ==========
    name_field = ft.TextField(label="Full Name", width=350)
    email_field = ft.TextField(label="Email", width=350)
    password_field = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=350
    )
    confirm_field = ft.TextField(
        label="Confirm Password", password=True, can_reveal_password=True, width=350
    )
    signup_error = ft.Text("", color="#FF0000")
    signup_success = ft.Text("", color="#00AA00")

    def signup_clicked(e):
        if password_field.value != confirm_field.value:
            signup_error.value = "Passwords do not match"
            signup_success.value = ""
        elif not email_field.value or not password_field.value or not name_field.value:
            signup_error.value = "Please fill all fields"
            signup_success.value = ""
        else:
            # check if email already exists
            rows = run_query(
                "SELECT id FROM teacher WHERE email=%s",
                [email_field.value],
                fetch=True,
            )
            if rows:
                signup_error.value = "Email already exists"
                signup_success.value = ""
            else:
                run_query(
                    "INSERT INTO teacher (email, display_name, password_hash) VALUES (%s, %s, %s)",
                    [email_field.value, name_field.value, password_field.value],
                )
                signup_error.value = ""
                signup_success.value = "Account created successfully!"
        page.update()

    signup_button = ft.ElevatedButton("Sign up", on_click=signup_clicked)
    back_to_login = ft.TextButton("Back to Login", on_click=lambda e: show_login())

    signup_view = ft.Column(
        [
            ft.Text("Create Teacher Account", size=22, weight="bold"),
            name_field,
            email_field,
            password_field,
            confirm_field,
            signup_button,
            signup_error,
            signup_success,
            back_to_login,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ========== DASHBOARD ==========
    def show_dashboard(teacher_name):
        question_prompt = ft.TextField(label="Question prompt", multiline=True, width=400)

        # main options
        allow_multiple = ft.Checkbox(label="Allow multiple submissions (up to 3)")
        hide_names = ft.Checkbox(label="Hide participant names when viewing responses")

        # play options
        play_title = ft.Text("Play Options", size=18, weight="bold")
        start_with_slide = ft.Checkbox(label="Start activity with slide")
        minimize_window = ft.Checkbox(label="Minimize activity window after activity starts")

        auto_close = ft.Checkbox(label="Auto-close submission after")
        auto_close_value = ft.TextField(
            hint_text="Enter number", width=100, input_filter=ft.NumbersOnlyInputFilter()
        )
        auto_close_unit = ft.Dropdown(
            options=[
                ft.dropdown.Option("sec"),
                ft.dropdown.Option("min"),
                ft.dropdown.Option("hour"),
            ],
            width=100,
        )

        # when clicking "Start collecting answers"
        def start_collecting(e):
            prompt = question_prompt.value
            allow = allow_multiple.value
            hide = hide_names.value

            # convert time to seconds if given
            seconds = None
            if auto_close.value and auto_close_value.value:
                try:
                    n = int(auto_close_value.value)
                    unit = auto_close_unit.value
                    if unit == "min":
                        seconds = n * 60
                    elif unit == "hour":
                        seconds = n * 3600
                    else:
                        seconds = n
                except:
                    seconds = None

            run_query(
                """
                INSERT INTO activity (session_id, prompt, allow_multiple, hide_names, auto_close_sec)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [1, prompt, allow, hide, seconds],  # temp session_id=1
            )

            page.snack_bar = ft.SnackBar(ft.Text("Question launched! Collecting answers..."))
            page.snack_bar.open = True
            page.update()

        start_button = ft.ElevatedButton("Start collecting answers", on_click=start_collecting)

        # options panel (hidden until teacher clicks button)
        options_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Question Options", size=20, weight="bold"),
                    question_prompt,
                    allow_multiple,
                    hide_names,
                    play_title,
                    start_with_slide,
                    minimize_window,
                    ft.Row([auto_close, auto_close_value, auto_close_unit]),
                    start_button,
                ],
                tight=True,
                spacing=8,
            ),
            bgcolor="#F0F0F0",
            padding=15,
            border_radius=10,
            visible=False,
            width=430,
        )

        def open_options_panel(e):
            options_panel.visible = True
            page.update()

        add_to_slide_btn = ft.FloatingActionButton(
            text="Add Question to Slide", on_click=open_options_panel
        )

        dashboard_view = ft.Column(
            [
                ft.Text(f"Welcome, {teacher_name}", size=22, weight="bold"),
                ft.Text("Click below to add a question to your slide."),
                add_to_slide_btn,
                options_panel,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        page.clean()
        page.add(dashboard_view)

    # start at login
    page.add(login_view)


ft.app(target=main)
