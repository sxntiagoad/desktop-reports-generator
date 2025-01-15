import flet as ft
import os
def main(page: ft.Page):
    page.title = "Merchants Dashboard"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#f8f9fa"
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.join(base_path, "assets", "logo_eva.png")

    
    def create_merchant_table():
        merchants_data = [
            {"name": "Love Wynnetal", "company": "Bobs Company", "id": "65245044", "status": "Active", "review": "In Review"},
        ] * 10  # Repeat the same data 10 times for demonstration
        
        table_headers = [
            "Legal Name",
            "DBA",
            "Merchant ID",
            "Contact Name",
            "KYC Status",
            "KYB Status",
            "",  # For manage button
        ]
        
        # Create header row
        header_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(header, size=12, color="#64748b", weight=ft.FontWeight.W_500),
                    width=130,
                )
                for header in table_headers
            ],
            spacing=5,
        )
        
        # Create table rows
        table_rows = []
        for merchant in merchants_data:
            row = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(merchant["name"], size=14),
                            width=130,
                        ),
                        ft.Container(
                            content=ft.Text(merchant["company"], size=14),
                            width=130,
                        ),
                        ft.Container(
                            content=ft.Text(merchant["id"], size=14),
                            width=130,
                        ),
                        ft.Container(
                            content=ft.Text(merchant["name"], size=14),
                            width=130,
                        ),
                        ft.Container(
                            content=ft.Text(
                                merchant["status"],
                                size=14,
                                color="#22c55e" if merchant["status"] == "Active" else "#64748b",
                            ),
                            width=130,
                        ),
                        ft.Container(
                            content=ft.Text(
                                merchant["review"],
                                size=14,
                                color="#3b82f6",
                            ),
                            width=130,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(
                                "Manage",
                                style=ft.ButtonStyle(
                                    color="white",
                                    bgcolor="#0ea5e9",
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                height=35,
                            ),
                            width=100,
                        ),
                    ],
                    spacing=5,
                ),
                bgcolor="white",
                padding=15,
                border_radius=8,
            )
            table_rows.append(row)
        
        return ft.Column(
            controls=[
                header_row,
                *table_rows,
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Showing 1 to 20 of 24 entries", size=12, color="#64748b"),
                            ft.Row(
                                controls=[
                                    ft.TextButton("Prev", style=ft.ButtonStyle(color="#64748b")),
                                    ft.TextButton("1", style=ft.ButtonStyle(color="#0ea5e9")),
                                    ft.TextButton("2", style=ft.ButtonStyle(color="#64748b")),
                                    ft.TextButton("3", style=ft.ButtonStyle(color="#64748b")),
                                    ft.TextButton("4", style=ft.ButtonStyle(color="#64748b")),
                                    ft.TextButton("5", style=ft.ButtonStyle(color="#64748b")),
                                    ft.TextButton("Next", style=ft.ButtonStyle(color="#64748b")),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Show Entries", size=12, color="#64748b"),
                                    ft.Dropdown(
                                        value="25",
                                        options=[
                                            ft.dropdown.Option("25"),
                                            ft.dropdown.Option("50"),
                                            ft.dropdown.Option("100"),
                                        ],
                                        width=70,
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.only(top=20),
                ),
            ],
            spacing=10,
        )
    logo_image=ft.Image(
        src=logo_path,
        width=40,
        height=40,
        fit=ft.ImageFit.CONTAIN,
    )
    # Sidebar
    sidebar = ft.Container(
        width=250,
        bgcolor="#1e293b",
        padding=20,
        content=ft.Column(
            controls=[
                ft.Container(
                    bgcolor="#F0F0F0",
                    border_radius=8,
                    content=ft.Row(
                        controls=[
                            logo_image,
                            ft.Text("Dashboard", color="white", size=16, weight=ft.FontWeight.W_500),
                        ],
                        spacing=10,
                    ),
                    margin=ft.margin.only(bottom=30),
                ),
                ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=icon, color="#94a3b8", size=20),
                                    ft.Text(text, color="#94a3b8", size=14),
                                ],
                                spacing=10,
                            ),
                            padding=10,
                            border_radius=8,
                        )
                        for icon, text in [
                            (ft.icons.DASHBOARD_OUTLINED, "Dashboard"),
                            (ft.icons.PEOPLE_OUTLINE, "Users"),
                            (ft.icons.SETTINGS_OUTLINED, "Settings"),
                            (ft.icons.INSERT_CHART_OUTLINED, "Reports"),
                            (ft.icons.CREDIT_CARD, "Underwriting"),
                            (ft.icons.PAYMENTS, "Settlements"),
                            (ft.icons.RATE_REVIEW, "Product Review"),
                            (ft.icons.SETTINGS, "Settings"),
                        ]
                    ],
                    spacing=5,
                ),
            ],
        ),
    )

    # Top Navigation Bar with Search
    navbar = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Merchants", size=24, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[
                                    ft.Text("Filter by:", size=14, color="#64748b"),
                                    ft.Dropdown(
                                        value="Active",
                                        options=[
                                            ft.dropdown.Option("Active"),
                                            ft.dropdown.Option("Inactive"),
                                            ft.dropdown.Option("All"),
                                        ],
                                        width=120,
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                ft.Container(
                    content=ft.TextField(
                        hint_text="Search merchant, Dealer ID etc",
                        prefix_icon=ft.icons.SEARCH,
                        border_radius=8,
                        bgcolor="white",
                        border_color="#e2e8f0",
                    ),
                    padding=ft.padding.only(top=20, bottom=20),
                ),
            ],
        ),
        padding=30,
        bgcolor="white",
    )

    # Main Content Area
    content_area = ft.Container(
        content=create_merchant_table(),
        padding=30,
        expand=True,
    )

    # Main Layout
    main_content = ft.Row(
        controls=[
            sidebar,
            ft.Container(
                content=ft.Column(
                    controls=[navbar, content_area],
                    spacing=0,
                ),
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )

    page.add(main_content)

if __name__ == "__main__":
    ft.app(target=main)