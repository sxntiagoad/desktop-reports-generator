import flet as ft

def main(page: ft.Page):
    page.title = "Dashboard"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#f5f5f5"
    
    def create_stat_card(title, value, change, icon):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(title, size=14, color=ft.colors.GREY_800),
                                ft.Icon(icon, color=ft.colors.BLUE, size=24),
                            ],
                        ),
                        ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            change,
                            size=12,
                            color=ft.colors.GREEN if "+" in change else ft.colors.RED,
                        ),
                    ],
                    spacing=5,
                ),
                padding=20,
                width=250,
            )
        )

    def create_chart_card():
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Sales Overview", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Text("Chart placeholder"),
                            height=300,
                            alignment=ft.alignment.center,
                        ),
                    ],
                ),
                width=600,
                padding=20,
            )
        )

    def create_activity_card():
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Recent Activity", size=16, weight=ft.FontWeight.BOLD),
                        ft.ListView(
                            controls=[
                                create_activity_item("New sale completed", "2 minutes ago"),
                                create_activity_item("New customer registered", "5 minutes ago"),
                                create_activity_item("Product updated", "1 hour ago"),
                                create_activity_item("Order shipped", "2 hours ago"),
                            ],
                            spacing=10,
                            height=300,
                        ),
                    ],
                ),
                width=400,
                padding=20,
            )
        )

    def create_activity_item(text, time):
        return ft.ListTile(
            leading=ft.CircleAvatar(
                content=ft.Icon(ft.icons.NOTIFICATIONS, color="white", size=15),
                bgcolor=ft.colors.BLUE,
                radius=15,
            ),
            title=ft.Text(text, size=14),
            subtitle=ft.Text(time, size=12, color=ft.colors.GREY_600),
        )

    def sidebar_item(icon, text, selected=False):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        icon,
                        color="white" if selected else ft.colors.BLUE_100,
                        size=20,
                    ),
                    ft.Text(
                        text,
                        color="white" if selected else ft.colors.BLUE_100,
                        size=14,
                        weight=ft.FontWeight.W_500
                    )
                ],
                spacing=15,
            ),
            bgcolor=ft.colors.BLUE_700 if selected else None,
            padding=15,
            border_radius=30 if selected else None,
            margin=ft.margin.only(left=20, right=20, top=5, bottom=5)
        )

    # Sidebar
    sidebar = ft.Container(
        width=250,
        height=page.height,
        bgcolor=ft.colors.BLUE_600,
        padding=ft.padding.only(top=20),
        content=ft.Column(
            controls=[
                # Logo section
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.icons.DASHBOARD_ROUNDED, color="white", size=25),
                            ft.Text("Dashboard", size=20, color="white", weight=ft.FontWeight.BOLD)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    margin=ft.margin.only(bottom=30)
                ),
                
                # Menu Items
                sidebar_item(ft.icons.DASHBOARD_OUTLINED, "Dashboard", selected=True),
                sidebar_item(ft.icons.SHOPPING_CART_OUTLINED, "Orders"),
                sidebar_item(ft.icons.PEOPLE_OUTLINE, "Customers"),
                sidebar_item(ft.icons.INVENTORY_2_OUTLINED, "Products"),
                sidebar_item(ft.icons.INSIGHTS_OUTLINED, "Analytics"),
                
                ft.Divider(color=ft.colors.BLUE_200, height=30),
                
                # Settings section
                ft.Container(
                    content=ft.Text("SETTINGS", size=12, color=ft.colors.BLUE_200),
                    margin=ft.margin.only(left=35, bottom=10, top=10)
                ),
                sidebar_item(ft.icons.PERSON_OUTLINE, "Profile"),
                sidebar_item(ft.icons.SETTINGS_OUTLINED, "Settings"),
            ],
            spacing=0,
        )
    )

    # Top Navigation Bar
    navbar = ft.Container(
        height=70,
        bgcolor="white",
        padding=ft.padding.all(15),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                # Search Bar
                ft.Container(
                    width=400,
                    height=45,
                    bgcolor=ft.colors.GREY_50,
                    border_radius=30,
                    padding=ft.padding.only(left=20, right=20),
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.SEARCH, color=ft.colors.GREY_400, size=20),
                            ft.TextField(
                                border=None,
                                hint_text="Buscar...",
                                hint_style=ft.TextStyle(color=ft.colors.GREY_400),
                                text_style=ft.TextStyle(color=ft.colors.GREY_800),
                                content_padding=ft.padding.only(left=10),
                                width=300,
                            )
                        ],
                        spacing=10,
                    )
                ),
                
                # Right side icons
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.NOTIFICATIONS_OUTLINED,
                            icon_color=ft.colors.GREY_700,
                            icon_size=20,
                            bgcolor=ft.colors.GREY_100,
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(),
                                padding=10,
                            )
                        ),
                        ft.IconButton(
                            icon=ft.icons.EMAIL_OUTLINED,
                            icon_color=ft.colors.GREY_700,
                            icon_size=20,
                            bgcolor=ft.colors.GREY_100,
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(),
                                padding=10,
                            )
                        ),
                        ft.Container(width=1, bgcolor=ft.colors.GREY_300, height=30),
                        ft.Row(
                            controls=[
                                ft.CircleAvatar(
                                    foreground_image_url="https://avatars.githubusercontent.com/u/5797983?v=4",
                                    radius=15,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("John Doe", size=14, weight=ft.FontWeight.W_500),
                                        ft.Text("Admin", size=12, color=ft.colors.GREY_700),
                                    ],
                                    spacing=0,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.ARROW_DROP_DOWN,
                                    icon_color=ft.colors.GREY_700,
                                )
                            ],
                            spacing=5,
                        )
                    ],
                    spacing=10,
                )
            ]
        )
    )

    # Main Content Area with Cards
    content_area = ft.Container(
        content=ft.Column(
            controls=[
                # Stats Cards Row
                ft.Row(
                    controls=[
                        create_stat_card("Total Sales", "$12,345", "+12%", ft.icons.TRENDING_UP),
                        create_stat_card("Total Revenue", "$98,765", "+8%", ft.icons.ATTACH_MONEY),
                        create_stat_card("New Customers", "321", "+15%", ft.icons.PERSON_ADD),
                        create_stat_card("Total Orders", "1,234", "+10%", ft.icons.SHOPPING_CART),
                    ],
                    spacing=20,
                ),
                
                # Chart and Recent Activity
                ft.Row(
                    controls=[
                        create_chart_card(),
                        create_activity_card(),
                    ],
                    spacing=20,
                ),
            ],
            spacing=20,
        ),
        padding=30,
        expand=True,
    )

    # Main Layout
    main_content = ft.Row(
        controls=[sidebar, 
                  ft.Container(
                      content=ft.Column(
                          controls=[navbar, content_area],
                          spacing=0,
                      ),
                      expand=True,
                  )],
        spacing=0,
        expand=True,
    )

    page.add(main_content)

if __name__ == "__main__":
    ft.app(target=main)
