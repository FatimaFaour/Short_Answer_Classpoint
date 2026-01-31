import flet as ft
from ..services.db import (
    get_answer_stats,
    get_common_answers,
    get_starred_answers,
)
from ..config import CARD, PRIMARY


def stat_card(title, value, icon):
    return ft.Container(
        width=180,
        padding=16,
        bgcolor=CARD,
        border_radius=16,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(icon, size=18),
                        ft.Text(title, size=12, color="#6B7280"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    str(value),
                    size=26,
                    weight="bold",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
    )


def section(title, content):
    return ft.Container(
        bgcolor=CARD,
        padding=20,
        border_radius=16,
        content=ft.Column(
            [
                ft.Text(title, size=16, weight="bold"),
                content,
            ],
            spacing=12,
        ),
    )


def summary_view(page, question, on_back, on_review):
    # ---- DATA ----
    answered, starred, avg_time, unique_answers = get_answer_stats(
        question["id"]
    )
    common_answers = get_common_answers(question["id"])
    starred_answers = get_starred_answers(question["id"])
    #clear_c, partial_c, weak_c = get_quality_breakdown(question["id"])

    # ---- HEADER ----
    header = ft.Row(
        [
            ft.TextButton("← Back", on_click=on_back),
            ft.Container(expand=True),
            ft.Text("Question Summary", size=22, weight="bold"),
            ft.Container(expand=True),
            ft.Text("⏱ 45s", size=14),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # ---- QUESTION CARD ----
    question_card = ft.Container(
        bgcolor=CARD,
        padding=20,
        border_radius=16,
        content=ft.Text(question["text"], size=16),
    )
    

    # ---- STATS ROW ----
    stats_row = ft.Row(
        [
            stat_card("Answered", answered, "👥"),
            stat_card("Starred", starred, "⭐"),
            stat_card("Unique", unique_answers, "🧠"),
            stat_card("Avg Time", f"{avg_time}s", "⏱"),
        ],
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
    )

    # ---- INSIGHT ----

    # ---- STARRED ANSWERS ----
    starred_list = ft.Column(
        [
            ft.Text(f"• {a}", size=14)
            for a in starred_answers
        ],
        spacing=8,
    )

    starred_section = section(
        "⭐ Starred Answers",
        starred_list if starred_answers else ft.Text("No starred answers."),
    )

    # ---- COMMON ANSWERS ----
    common_list = ft.Column(
        [
            ft.Row(
                [
                    ft.Text(answer, expand=True),
                    ft.Text(str(count), weight="bold"),
                ]
            )
            for answer, count in common_answers
        ],
        spacing=6,
    )

    common_section = section(
        "🧠 Common Answers",
        common_list if common_answers else ft.Text("No repeated answers."),
    )

    # ---- QUALITY BREAKDOWN ----
    #quality_row = ft.Row(
    #    [
    #        stat_card("Clear", clear_c, "🟢"),
    #        stat_card("Partial", partial_c, "🟡"),
    #        stat_card("Weak", weak_c, "🔴"),
    #    ],
    #    spacing=16,
    #)

    # ---- ACTIONS ----
    actions = ft.Row(
    [
        ft.OutlinedButton(
            "👁 Review Answers",
            on_click=lambda e: on_review(question),
        ),
    ],
    alignment=ft.MainAxisAlignment.END,
)


    # ---- FINAL LAYOUT ----
    return ft.Column(
        [
            header,
            question_card,
            stats_row,
            ft.Row(
                [
                    starred_section,
                    common_section,
                ],
                spacing=16,
            ),
            #quality_row,
            actions,
        ],
        spacing=24,
        expand=True,
    )
