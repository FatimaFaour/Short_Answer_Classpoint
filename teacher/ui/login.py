import flet as ft
from ..services.db import get_teacher_by_email

def login_view(page, on_success):
    email = ft.TextField(label="Email", width=360, border_radius=12)
    error = ft.Text(color="red")

    def login(e):
        rows = get_teacher_by_email(email.value)
        if rows:
            on_success(*rows[0])
        else:
            error.value = "Teacher not found"
            page.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Teacher Login", size=26, weight="bold"),
                email,
                ft.ElevatedButton("Login", on_click=login),
                error,
            ],
            spacing=16,
            horizontal_alignment="center",
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
    )
