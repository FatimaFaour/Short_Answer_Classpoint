import flet as ft
from ..services.api import get_answers
from .answer_card import answer_card
from ..config import CARD



def review_answers_view(page, question, on_back):
    answers_column = ft.Column(spacing=10)

    def load_answers():
        answers_column.controls.clear()
        answers = get_answers(question["id"])
        #clusters = cluster_answers(answers)

        
        for a in answers:
            answers_column.controls.append(
                answer_card(a, refresh=load_answers)
            )
        page.update()

    load_answers()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.TextButton("← Back", on_click=on_back),
                    ft.Text("Review Answers", size=22, weight="bold"),
                ]
            ),
            ft.Container(
                bgcolor=CARD,
                padding=20,
                border_radius=16,
                content=answers_column,
                expand=True,
            ),
        ],
        spacing=16,
        expand=True,
    )
