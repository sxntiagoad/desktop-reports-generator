import flet as ft
from app.presentation.login import main as login_page
from app.presentation.dashboard import main as dashboard_page
from app.models.user import CurrentUser

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_user = CurrentUser()
        
        # Iniciar con la página de login
        login_page(self.page)
        
        # Configurar el manejador de rutas
        self.page.on_route_change = self.handle_route_change

    def handle_route_change(self, e):
        if e.route == "/dashboard":
            if self.current_user.is_authenticated:
                self.page.clean()
                dashboard_page(self.page)
            else:
                self.page.go("/")  # Redirigir a login si no está autenticado
        elif e.route == "/" or not e.route:
            self.page.clean()
            login_page(self.page)

def main(page: ft.Page):
    return Router(page)

if __name__ == "__main__":
    ft.app(target=main)
