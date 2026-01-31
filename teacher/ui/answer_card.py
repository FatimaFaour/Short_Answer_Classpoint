import flet as ft
from ..services.api import toggle_star


def answer_card(answer, refresh=None):
    def on_toggle(e):
        toggle_star(answer["id"])
        answer["starred"] = e.control.value
        if refresh:
            refresh()

    return ft.Container(
        padding=12,
        border_radius=12,
        bgcolor="#F9FAFB",
        content=ft.Row(
            [
                ft.Checkbox(
                    value=answer.get("starred", False),
                    on_change=on_toggle,
                ),
                ft.Column(
                    [
                        ft.Text(answer["name"], weight="bold"),
                        ft.Text(answer["text"]),
                    ],
                    expand=True,
                ),
            ],
            spacing=12,
        ),
    )
