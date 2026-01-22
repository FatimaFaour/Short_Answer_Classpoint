import flet as ft
from ..config import CARD, PRIMARY

def setup_view(page, state, on_start):
    allow_multiple = ft.Checkbox(label="Allow multiple submissions (up to 3)")
    hide_names = ft.Checkbox(label="Hide participant names when viewing responses")

    auto_close = ft.Checkbox(label="Auto-close submission after")
    auto_close_seconds = ft.Dropdown(
        width=120,
        options=[ft.dropdown.Option(str(i)) for i in [30, 60, 90, 120]],
        disabled=True,
    
    )

    def toggle_auto_close(e):
        auto_close_seconds.disabled = not auto_close.value
        page.update()

    auto_close.on_change = toggle_auto_close

    def start_activity(e):
        state.allow_multiple = allow_multiple.value
        state.max_submissions = 3 if allow_multiple.value else 1
        state.hide_names = hide_names.value
        state.auto_close_seconds = (
            int(auto_close_seconds.value)
            if auto_close.value and auto_close_seconds.value
            else None
        )
        on_start()

    return ft.Container(
        padding=24,
        bgcolor=CARD,
        border_radius=16,
        width=420,
        content=ft.Column(
            [
                ft.Text("Short Answer", size=20, weight="bold"),
                ft.Divider(),

                allow_multiple,
                hide_names,

                ft.Text("Play Options", weight="bold"),
                auto_close,
                auto_close_seconds,

                ft.Container(height=20),

                ft.ElevatedButton(
                    "View Responses",
                    bgcolor=PRIMARY,
                    color="white",
                    on_click=start_activity,
                ),
            ],
            spacing=14,
        ),
    )
