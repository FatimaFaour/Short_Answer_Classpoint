import flet as ft
from ..config import CARD
from ..services.db import get_answers, toggle_star

def refresh_answers(page, answers_column, question_id, hide_names=False):
    answers = get_answers(question_id)
    answers_column.controls.clear()

    for a in answers:
        name = "Anonymous" if hide_names else a["name"]

        answers_column.controls.append(
            ft.Container(
                bgcolor=CARD,
                border_radius=16,
                padding=14,
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(name, weight="bold"),
                                ft.Text(a["text"], size=14),
                            ],
                            expand=True,
                        ),
                        ft.Checkbox(
                            value=a["starred"],
                            on_change=lambda e, aid=a["id"]: (
                                toggle_star(aid),
                                refresh_answers(
                                    page, answers_column, question_id, hide_names
                                ),
                            ),
                        ),
                    ],
                ),
            )
        )

    page.update()
    return len(answers)
