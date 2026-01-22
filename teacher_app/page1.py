import flet as ft

# Constants
PRIMARY = "#6366F1"
BG = "#F9FAFB"
CARD_BG = "#FFFFFF"
TEXT = "#0F172A"
MUTED = "#64748B"
WHITE = "#FFFFFF"
GREEN = "#22C55E"

def stat_card(title, value, highlight=False):
    return ft.Container(
        bgcolor=CARD_BG,
        border_radius=12,
        padding=30,
        expand=True,
        border=ft.border.all(1, "#E2E8F0"),
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(title.upper(), size=12, color=MUTED, weight=ft.FontWeight.W_600),
                ft.Text(
                    value,
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=PRIMARY if highlight else TEXT,
                ),
            ],
        ),
    )

def class_row(icon, icon_bg, title, code, students):
    return ft.Container(
        bgcolor=CARD_BG,
        border_radius=16,
        padding=20,
        border=ft.border.all(1, "#E2E8F0"),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=20,
                    controls=[
                        ft.Container(
                            width=48, height=48,
                            bgcolor=icon_bg,
                            border_radius=10,
                            alignment=ft.Alignment(0, 0),
                            content=ft.Icon(icon, color=PRIMARY, size=24),
                        ),
                        ft.Column(
                            spacing=8,
                            controls=[
                                ft.Text(title, size=18, weight=ft.FontWeight.W_700),
                                ft.Row(
                                    spacing=15,
                                    controls=[
                                        ft.Container(
                                            bgcolor="#F1F5F9",
                                            padding=ft.padding.symmetric(6, 12),
                                            border_radius=8,
                                            content=ft.Row([
                                                ft.Icon("key", size=14, color=MUTED),
                                                ft.Text(f"Code: {code}", size=13, weight="bold")
                                            ], spacing=5)
                                        ),
                                        ft.Row([
                                            ft.Container(width=8, height=8, bgcolor=GREEN, shape=ft.BoxShape.CIRCLE),
                                            ft.Text(f"{students} Students Active", size=12, color=MUTED)
                                        ], spacing=5)
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.TextButton("End Session", style=ft.ButtonStyle(color=MUTED)),
                        ft.Button(
                            "View Session",
                            bgcolor=PRIMARY,
                            color=WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            height=45
                        ),
                    ]
                )
            ]
        )
    )

def main(page: ft.Page):
    page.bgcolor = WHITE
    page.title = "ClassPoint Dashboard"
    page.window_width = 1300
    page.window_height = 900
    page.padding = 0

    # SIDEBAR
    sidebar = ft.Container(
        width=240,
        padding=ft.padding.only(top=20, left=15, right=15, bottom=20),
        border=ft.border.only(right=ft.BorderSide(1, "#E2E8F0")),
        content=ft.Column(
            controls=[
                # Logo
                ft.Row([
                    ft.Container(bgcolor=PRIMARY, width=32, height=32, border_radius=8, content=ft.Icon("school", color="white", size=18)),
                    ft.Text("ClassPoint", size=20, weight="bold")
                ], spacing=10),
                ft.Container(height=20),
                # Nav Items
                ft.Container(
                    bgcolor="#EEF2FF", border_radius=8, padding=12,
                    content=ft.Row([ft.Icon("grid_view", color=PRIMARY, size=20), ft.Text("Classes", color=PRIMARY, weight="bold")], spacing=12)
                ),
                ft.ListTile(leading=ft.Icon("help_outline", color=MUTED), title=ft.Text("Questions", color=MUTED)),
                ft.ListTile(leading=ft.Icon("bar_chart", color=MUTED), title=ft.Text("Reports", color=MUTED)),
                ft.ListTile(leading=ft.Icon("settings", color=MUTED), title=ft.Text("Settings", color=MUTED)),
                ft.Container(expand=True),
                # Profile
                ft.Container(
                    bgcolor="#F1F5F9", border_radius=12, padding=12,
                    content=ft.Row([
                        #ft.CircleAvatar(src="https://flet.dev/img/pages/docs/controls/circle-avatar/avatar.png"),                        
                        ft.Column([
                            ft.Text("Prof. Sarah Jenkins", size=13, weight="bold"),
                            ft.Text("Premium Account", size=11, color=MUTED)
                        ], spacing=0)
                    ])
                )
            ]
        )
    )

    # MAIN CONTENT
    content_col = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=25,
        controls=[
            # Header
            ft.Row([
                ft.Text("Management Dashboard", size=18, weight="w600"),
                ft.Row([ft.Icon("dark_mode_outlined", size=20), ft.Icon("notifications_outlined", size=20)], spacing=15)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            # Title Section
            ft.Row([
                ft.Column([
                    ft.Text("Active Classes", size=28, weight="bold"),
                    ft.Text("Manage your current active sessions and generate codes.", color=MUTED)
                ], spacing=5),
                ft.Button(
                    "Generate New Class Code",
                    icon="add",
                    bgcolor=PRIMARY,
                    color="white",
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            # Stats
            ft.Row([
                stat_card("Total Students", "128"),
                stat_card("Active Sessions", "4", True),
                stat_card("Responses Today", "842"),
            ], spacing=20),

            # Classes List
            class_row("science", "#EEF2FF", "Physics 101 - Advanced Mechanics", "482910", 32),
            class_row("calculate", "#EFF6FF", "Calc II - Integral Calculus", "772103", 28),
            class_row("history_edu", "#FFFBEB", "Modern World History", "110945", 45),

            # Dotted Guest Session Area
            ft.Container(
                height=180,
                border_radius=16,
                border=ft.border.all(2, "#E2E8F0"), # Note: Flet 0.80.2 dash support is via custom paint, using solid for now
                padding=30,
                content=ft.Column([
                    ft.Container(bgcolor="#F1F5F9", width=40, height=40, border_radius=20, content=ft.Icon("add", color=MUTED)),
                    ft.Text("Ready to start another class?", weight="bold", size=16),
                    ft.TextButton("Generate a new temporary code for a guest session", style=ft.ButtonStyle(color=PRIMARY))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
            ),
            
            # Bottom Hint
            ft.Row([
                ft.Icon("lightbulb_outline", color="#F59E0B", size=20),
                ft.Text("Hint: You can find detailed activity examples and tutorials in our resource center.", size=13, color=MUTED)
            ], spacing=10)
        ]
    )

    page.add(
        ft.Row([
            sidebar,
            ft.Container(content=content_col, expand=True, padding=ft.padding.all(40), bgcolor=BG)
        ], expand=True, spacing=0)
    )

ft.app(target=main)