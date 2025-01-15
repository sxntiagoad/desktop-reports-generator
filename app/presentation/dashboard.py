import flet as ft
from app.models.user import CurrentUser

def main(page: ft.Page):

    page.title = "Dashboard"
    page.add(ft.Text(f"Bienvenido,ff"))

if __name__ == "__main__":
    ft.app(target=main)
