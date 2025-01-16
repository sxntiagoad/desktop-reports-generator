import flet as ft
import os
from app.controllers.auth_controller import AuthController
from firebase_admin import auth as firebase_auth
import asyncio

# Obtener la ruta base del proyecto
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logo_path = os.path.join(base_path, "assets", "logo_eva.png")

def main(page: ft.Page):
    page.title = "EVA - Sistema de Informes"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE
    page.window.min_width = 900
    page.window.min_height = 600
    page.expand = True

    # Inicializar controlador
    auth_controller = AuthController()

    # Estado para loading
    loading = ft.ProgressRing(
        width=16, 
        height=16, 
        stroke_width=2,
        color=ft.Colors.BLUE,
        visible=True
    )

    # Snackbar personalizado y moderno
    success_snackbar = ft.SnackBar(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE_ROUNDED,
                        color=ft.Colors.GREEN_600,
                        size=20,
                    ),
                    ft.Text(
                        "¡Inicio de sesión exitoso!",
                        color=ft.Colors.GREEN_900,
                        size=14,
                        weight=ft.FontWeight.W_500,
                        style=ft.TextStyle(font_family="Poppins-Medium"),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
        ),
        bgcolor=ft.Colors.WHITE,
        duration=2000,
        behavior=ft.SnackBarBehavior.FLOATING,
    )

    error_text = ft.Text("", color="red", size=12, visible=False)

    # Diálogo de progreso suave y minimalista
    loading_dialog = ft.AlertDialog(
        modal=True,
        content=ft.Container(
            height=60,
            width=40,
            content=ft.ProgressRing(
                width=30,
                height=30,
                stroke_width=2,
                color=ft.colors.BLUE_400,
            ),
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.2, ft.colors.GREY_800),
                offset=ft.Offset(0, 0),
            ),
            alignment=ft.alignment.center,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        ),
        bgcolor=ft.colors.TRANSPARENT,
        shape=ft.RoundedRectangleBorder(radius=8),
        inset_padding=0,
    )

    async def login(e):
        # Mostrar el diálogo de carga
        page.dialog = loading_dialog
        loading_dialog.open = True
        page.update()

        # Limpiar el mensaje de error antes de intentar iniciar sesión
        error_text.visible = False
        error_text.value = ""

        email = email_input.value
        password = password_input.value

        if not email or not password:
            await asyncio.sleep(0.7)  # Tiempo mínimo de visualización
            loading_dialog.open = False
            error_text.value = "Por favor completa todos los campos"
            error_text.visible = True
            page.update()
            return

        try:
            user = auth_controller.login(email, password)
            await asyncio.sleep(0.7)  # Tiempo mínimo de visualización
            
            if user:
                # Cerrar el diálogo
                loading_dialog.open = False
                page.update()
                
                # Mostrar el snackbar y redirigir
                page.show_snack_bar(success_snackbar)
                await asyncio.sleep(0.1)  # Pequeña pausa para asegurar que el diálogo se cierre
                page.go("/dashboard")  # Asegúrate de que esta ruta sea correcta
            else:
                loading_dialog.open = False
                error_text.value = "Credenciales inválidas"
                error_text.visible = True
                page.update()
        except Exception as e:
            await asyncio.sleep(0.7)
            loading_dialog.open = False
            error_text.value = "Error en la autenticación"
            error_text.visible = True
            page.update()

    def handle_resize(e):
        width = page.window.width
        height = page.window.height
        is_mobile = width < 900
        
        if is_mobile:
            main_row.vertical = True
            welcome_container.width = width
            welcome_container.height = None
            login_container.width = width
            login_container.height = None
        else:
            main_row.vertical = False
            welcome_container.width = width * 0.5
            welcome_container.height = None
            login_container.width = width * 0.5
            login_container.height = None

        # Ajustar padding
        padding_size = min(width * 0.05, 40)
        welcome_content.padding = ft.padding.all(padding_size)
        login_form.padding = ft.padding.all(padding_size)
        
        page.update()

    def on_window_event(e):
        if e.data == "resize":
            handle_resize(e)

    page.window.on_event = on_window_event

    # Panel de bienvenida
    welcome_text = ft.Text(
        "Bienvenido al Sistema\nde Informes EVA",
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        style=ft.TextStyle(font_family="BB Anonym"),
        size=28,
    )
    
    description_text = ft.Text(
        "Genera y gestiona tus informes\nde manera rápida y eficiente",
        color=ft.Colors.WHITE70,
        text_align=ft.TextAlign.CENTER,
        size=16,
    )

    welcome_content = ft.Container(
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                welcome_text,
                description_text,
            ],
        ),
        expand=True
    )

    # Logo
    logo_image = ft.Image(
        src=logo_path,
        width=120,
        height=120,
        fit=ft.ImageFit.CONTAIN,
    )

    # Campos del formulario
    email_input = ft.TextField(
        label="Correo electrónico",
        border=ft.InputBorder.UNDERLINE,
        width=300,
        text_size=14,
        hint_text="ejemplo@eva.com",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        hint_style=ft.TextStyle(
            color=ft.Colors.GREY_400,
            size=12,
        ),
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_700,
            size=14,
            weight=ft.FontWeight.W_500,
        ),
        focused_border_color=ft.Colors.BLUE,
        focused_color=ft.Colors.BLUE,
        border_color=ft.Colors.GREY_300,
        cursor_color=ft.Colors.BLUE,
        selection_color=ft.Colors.BLUE_50,
        bgcolor=ft.Colors.WHITE,
    )

    def toggle_password_visibility(e):
        password_input.password = not password_input.password
        e.control.icon = ft.Icons.VISIBILITY_OFF if password_input.password else ft.Icons.VISIBILITY
        e.control.update()
        password_input.update()

    password_input = ft.TextField(
        label="Contraseña",
        border=ft.InputBorder.UNDERLINE,
        password=True,
        width=300,
        text_size=14,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        hint_text="Ingresa tu contraseña",
        hint_style=ft.TextStyle(
            color=ft.Colors.GREY_400,
            size=12,
        ),
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_700,
            size=14,
            weight=ft.FontWeight.W_500,
        ),
        focused_border_color=ft.Colors.BLUE,
        focused_color=ft.Colors.BLUE,
        border_color=ft.Colors.GREY_300,
        cursor_color=ft.Colors.BLUE,
        selection_color=ft.Colors.BLUE_50,
        bgcolor=ft.Colors.WHITE,
        suffix_icon=ft.IconButton(
            icon=ft.Icons.VISIBILITY_OFF,
            icon_color=ft.Colors.GREY_600,
            icon_size=20,
            on_click=toggle_password_visibility,
            style=ft.ButtonStyle(
                color=ft.Colors.GREY_700,
                padding=8,
            ),
        ),
    )

    login_title = ft.Text(
        "Iniciar Sesión",
        weight=ft.FontWeight.BOLD,
        size=24,
        font_family="BB Anonym",
    )

    # Botón de inicio de sesión con loading
    login_button = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Text(
                    "INICIAR SESIÓN",
                    size=14,
                    weight=ft.FontWeight.W_500,
                ),
                loading,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=50, vertical=20),
        ),
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE,
        on_click=login,
        width=300,
    )

    # Formulario de login
    login_form = ft.Container(
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                logo_image,
                login_title,
                email_input,
                password_input,
                error_text,
                login_button,
            ],
        ),
        padding=40,
        expand=True
    )

    # Welcome container con altura completa
    welcome_container = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#1E88E5", "#1976D2"],
        ),
        content=welcome_content,
        alignment=ft.alignment.center,
        expand=True,
        margin=0,
        padding=0,
    )

    # Login container con altura completa
    login_container = ft.Container(
        bgcolor=ft.Colors.WHITE,
        content=login_form,
        alignment=ft.alignment.center,
        expand=True,
        margin=0,
        padding=0,
    )

    # Main row que ocupa todo el espacio
    main_row = ft.Row(
        controls=[
            welcome_container,
            login_container
        ],
        spacing=0,
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    # Contenedor principal que ocupa toda la pantalla
    main_container = ft.Container(
        content=main_row,
        expand=True,
        margin=0,
        padding=0,
    )

    page.add(main_container)
    handle_resize(None)

if __name__ == "__main__":
    ft.app(target=main)