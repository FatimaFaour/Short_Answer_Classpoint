import flet as ft
from ..services.db import (
    create_teacher,
    get_teacher_by_credentials,
    get_teacher_by_email,
)

def login_view(page, on_success):
    # ================= PAGE STYLE =================
    page.bgcolor = "#CDCEEC"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"

    mode = {"value": "login"}  # login | signup
    error = ft.Text(color="#DC2626", size=12)

    # ================= INPUT FIELDS =================
    def styled_input(label, password=False):
        return ft.TextField(
            label=label,
            width=360,
            height=50,
            border_radius=14,
            filled=True,
            bgcolor="#FAFAFA",
            password=password,
            can_reveal_password=password,
        )

    email = styled_input("Email")
    password = styled_input("Password", password=True)
    name = styled_input("Name")
    confirm_password = styled_input("Confirm password", password=True)

    name.visible = False
    confirm_password.visible = False

    title = ft.Text(size=26, weight="bold")
    subtitle = ft.Text(
        size=13,
        color="#6B7280",
        text_align="center",
    )

    # ================= ACTIONS =================
    def submit(e):
        error.value = ""

        if mode["value"] == "login":
            if not email.value or not password.value:
                error.value = "Enter your email and password"
                page.update()
                return

            rows = get_teacher_by_credentials(email.value, password.value)
            if rows:
                on_success(*rows[0])
            else:
                error.value = "Invalid email or password"
                page.update()

        else:  # signup
            if not name.value or not email.value or not password.value:
                error.value = "Please fill all fields"
                page.update()
                return

            if password.value != confirm_password.value:
                error.value = "Passwords do not match"
                page.update()
                return

            if get_teacher_by_email(email.value):
                error.value = "An account already exists with this email"
                page.update()
                return

            rows = create_teacher(name.value, email.value, password.value)
            if rows:
                on_success(*rows[0])

    def switch_mode(e):
        error.value = ""

        if mode["value"] == "login":
            mode["value"] = "signup"
            title.value = "Create your account"
            subtitle.value = "Start using Short Answer in seconds"
            name.visible = True
            confirm_password.visible = True
            submit_btn.text = "Create account"
            switch_text.value = "Already have an account? Sign in"
        else:
            mode["value"] = "login"
            title.value = "Welcome back 👋"
            subtitle.value = "Sign in to start your session"
            name.visible = False
            confirm_password.visible = False
            submit_btn.text = "Sign in"
            switch_text.value = "Don’t have an account? Create one"

        page.update()

    # ================= BUTTONS =================
    submit_btn = ft.ElevatedButton(
        "Sign in",
        width=360,
        height=48,
        style=ft.ButtonStyle(
            bgcolor="#6366F1",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=14),
            elevation=0,
        ),
        on_click=submit,
    )

    switch_text = ft.TextButton(
        "Don’t have an account? Create one",
        on_click=switch_mode,
    )

    # ================= INITIAL TEXT =================
    title.value = "Welcome back 👋"
    subtitle.value = "Sign in to start your session"

    # ================= CARD =================
    card = ft.Container(
        width=420,
        padding=ft.padding.all(32),
        bgcolor="white",
        border_radius=20,
        shadow=ft.BoxShadow(
            blur_radius=30,
            color="black",
            offset=ft.Offset(0, 12),
        ),
        content=ft.Column(
            [
                title,
                subtitle,
                ft.Container(height=24),
                email,
                password,
                name,
                confirm_password,
                ft.Container(height=8),
                submit_btn,
                error,
                ft.Divider(height=32),
                switch_text,
            ],
            spacing=14,
            horizontal_alignment="center",
        ),
    )

    # ================= ROOT =================
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=card,
    )
