import flet as ft
import random
import string
from teacher.connect import run_query
from pathlib import Path
from flet_webview import WebView

PRIMARY = "#6366F1"
BG = "#FAFAF9"


def generate_code():
    return "".join(random.choices(string.digits, k=5))


def main(page: ft.Page):
    page.title = "Teacher Login | ClassPoint"
    page.window_width = 1200
    page.window_height = 800
    page.bgcolor = BG
    page.padding = 20

    # ---------------- LOGIN FIELDS ----------------
    email = ft.TextField(
        label="Email Address",
        width=360,
        border_radius=12,
        prefix_icon="mail_outline",
        hint_text="teacher@school.edu",
    )

    password = ft.TextField(
        label="Password",
        width=360,
        border_radius=12,
        password=True,
        can_reveal_password=True,
        prefix_icon="lock_open",
        hint_text="••••••••",
    )

    remember_me = ft.Checkbox(label="Keep me logged in for 30 days")

    error = ft.Text(color="red")

    def login(e):
        rows = run_query(
            "SELECT id, name FROM teachers WHERE email=%s",
            [email.value],
            fetch=True
        )

        if rows:
            teacher_id, name = rows[0]
            show_dashboard_html(teacher_id, name)
        else:
            error.value = "Invalid email or password"
            page.update()

    # ---------------- LOGIN VIEW ----------------
    login_view = ft.Container(
        content=ft.Column(
            [
                ft.Text("Welcome Back", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Please enter your details to sign in.",
                    size=14,
                    color="#64748B",
                ),

                email,

                ft.Column(
                    [
                        ft.Row(
                                [
                                    ft.Text("Password", weight=ft.FontWeight.BOLD),
                                    ft.TextButton("Forgot Password?"),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                width=360,
                            ),

                        password,
                    ],
                    spacing=4,
                ),

                remember_me,

                ft.ElevatedButton(
                    "Sign In",
                    width=360,
                    height=45,
                    bgcolor=PRIMARY,
                    color="white",
                    on_click=login,
                ),

                ft.Row(
                    [
                        ft.Divider(expand=True),
                        ft.Text(
                            "Or continue with",
                            size=12,
                            color="#64748B",
                        ),
                        ft.Divider(expand=True),
                    ],
                    width=360,
                ),

                ft.Row(
                    [
                        ft.OutlinedButton("Google", width=170),
                        ft.OutlinedButton("Microsoft", width=170),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=360,
                ),

                ft.Row(
                    [
                        ft.Text("New to the platform?"),
                        ft.TextButton("Create an account"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),

                error,
            ],
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
    )

    page.add(login_view)

    # ---------------- HTML DASHBOARD ----------------
    def show_dashboard_html(teacher_id, teacher_name):
        page.clean()
        code = generate_code()

        html_path = Path("teacher_app/ui/dashboard.html").resolve()
        page.add(
            WebView(
                url=html_path.as_uri(),
                expand=True,
            )
        )


ft.app(target=main)
