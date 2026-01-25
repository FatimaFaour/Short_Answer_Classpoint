import flet as ft
from ..services.db import get_answer_stats
from ..config import CARD, PRIMARY

def summary_view(page, question, on_back):
    answered, starred = get_answer_stats(question["id"])

    stat_card = lambda title, value: ft.Container(
        width=200,
        padding=20,
        bgcolor=CARD,
        border_radius=16,
        content=ft.Column(
            [
                ft.Text(title, size=12, color="#6B7280"),
                ft.Text(str(value), size=28, weight="bold"),
            ],
            horizontal_alignment="center",
        ),
    )

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Question Summary", size=22, weight="bold"),
                    ft.Container(expand=True),
                    ft.TextButton("← Back", on_click=on_back),
                ]
            ),

            ft.Text(question["text"], size=16),

            ft.Row(
                [
                    stat_card("Answered", answered),
                    stat_card("Starred", starred),
                ],
                spacing=16,
            ),
        ],
        spacing=24,
    )
