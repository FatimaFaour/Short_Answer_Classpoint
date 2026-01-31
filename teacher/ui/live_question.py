import flet as ft
import time
import asyncio
from ..services.api import get_answers, toggle_star
from ..config import CARD, PRIMARY


def live_question_view(page, state, on_close):
    # ---------- HEADER STATS ----------
    submissions_text = ft.Text("0", size=16, weight="bold")
    timer_text = ft.Text("00:00", size=16, weight="bold")

    # ---------- RESPONSES AREA ----------
    responses_column = ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    def build_answer_card(a):
        def on_toggle(e):
            toggle_star(a["id"])
            a["starred"] = e.control.value

        return ft.Container(
        expand=True,
        padding=14,
        bgcolor=CARD,
        border_radius=14,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Checkbox(
                            value=a.get("starred", False),
                            on_change=on_toggle,
                        ),
                        ft.Text(
                            a["text"],
                            size=14,
                            expand=True,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Divider(),
                ft.Text(
                    a["name"] if not state.hide_names else "Anonymous",
                    size=12,
                    color="#6b7280",
                ),
            ],
            spacing=6,
        ),
    )


    # ---------- UPDATE UI ----------
    def update_ui():
        if not state.current_question_id or not page.controls:
            return

        # Timer
        elapsed = int(time.time() - state.question_start_ts)
        timer_text.value = f"{elapsed//60:02d}:{elapsed%60:02d}"

        answers = get_answers(state.current_question_id)
        submissions_text.value = str(len(answers))

        responses_column.controls.clear()

        row_cards = []
        for a in answers:
            card = build_answer_card(a)


            row_cards.append(card)

            # 2 cards per row
            if len(row_cards) == 2:
                responses_column.controls.append(
                    ft.Row(row_cards, spacing=16)
                )
                row_cards = []

        # leftover single card
        if row_cards:
            responses_column.controls.append(
                ft.Row(row_cards, spacing=16)
            )

        page.update()

    # ---------- AUTO REFRESH ----------
    async def auto_refresh():
        while state.current_question_id:
            await asyncio.sleep(1)
            update_ui()

    update_ui()
    page.run_task(auto_refresh)

    # ---------- HEADER ----------
    header = ft.Container(
        padding=16,
        bgcolor="white",
        border_radius=12,
        content=ft.Row(
            [
                ft.Text("Short Answer", size=20, weight="bold"),
                ft.Container(expand=True),
                ft.Text("Code"),
                ft.Text(
                    state.session_code,
                    size=18,
                    weight="bold",
                    color=PRIMARY,
                ),
                ft.Row(
                    [
                        ft.Container(
                            width=8,
                            height=8,
                            bgcolor=PRIMARY,
                            border_radius=4,
                        ),
                        ft.Text("Live", color=PRIMARY, weight="bold"),
                    ],
                    spacing=6,
                ),
            ],
        ),
    )

    # ---------- SEARCH BAR (visual only) ----------
    #search_bar = ft.Container(
    #    padding=12,
    #    content=ft.Row(
    #        [
    #            ft.TextField(
    #                hint_text="⌕ Search name or answer",
    #                border_radius=20,
    #                expand=True,
    #            ),
    #            ft.Text("Showing"),
    #            submissions_text,
    #            ft.Text("responses"),
    #        ],
    #    ),
    #)

    # ---------- FOOTER ----------
    footer = ft.Container(
        padding=16,
        bgcolor="white",
        content=ft.Row(
            [
                ft.Text("👥"),
                submissions_text,
                ft.Text("⏱"),
                timer_text,
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Close submissions",
                    bgcolor="#4143A4",
                    color="white",
                    on_click=on_close,
                ),
            ],
        ),
    )

    # ---------- FINAL LAYOUT ----------
    return ft.Column(
        [
            header,
            search_bar,
            responses_column,
            footer,
        ],
        expand=True,
        spacing=0,
    )


async def auto_refresh(page, callback):
    while True:
        await asyncio.sleep(1)
        callback()
