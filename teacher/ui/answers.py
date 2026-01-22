import flet as ft
from ..config import CARD, PRIMARY
from ..services.api import get_answers, star_answer

def refresh_answers(page, answers_column, question_id, hide_names=False):
    answers = get_answers(question_id)
    

    answers_column.controls.clear()

    for a in answers:
        name = "Anonymous" if hide_names else a["name"]
        def toggle_star(e, answer_id=a["id"]):
            star_answer(answer_id)
            refresh_answers(page, answers_column, question_id, hide_names)
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
            value=a.get("starred", False),
            on_change=lambda e, aid=a["id"]: (
    star_answer(aid),
    refresh_answers(page, answers_column, question_id, hide_names)
),
        ),
    ],
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
),
            )
        )

    page.update()
    return len(answers)
