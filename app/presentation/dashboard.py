import flet as ft
from datetime import datetime, timedelta
from app.controllers.report_controller import ReportController
from app.presentation.widgets.data_table import create_data_table  # Asegúrate de que este módulo exista

def main(page: ft.Page):
    report_controller = ReportController()

    # Configuración de la página
    page.title = "Merchants Dashboard"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#f8f9fa"

    # Sidebar
    sidebar = ft.Container(
        width=250,
        bgcolor="#1e293b",
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Dashboard", color="white", size=16, weight=ft.FontWeight.W_500),
                # Agrega más controles al sidebar aquí
            ],
        ),
    )

    # Crear componentes de selección de fechas
    start_date = ft.DatePicker(
        help_text="Desde la fecha:",
        first_date=datetime(2024, 1, 1),
        last_date=datetime(2030, 12, 31)
    )
    
    end_date = ft.DatePicker(
        help_text="Hasta la fecha:",
        first_date=datetime(2024, 1, 1),
        last_date=datetime(2030, 12, 31)
    )

    # Validar el rango de fechas
    def validate_date_range():
        if start_date.value and end_date.value:
            try:
                # Convertir a datetime si es string
                if isinstance(start_date.value, str):
                    start = datetime.strptime(start_date.value, "%Y-%m-%d")
                else:
                    start = start_date.value

                if isinstance(end_date.value, str):
                    end = datetime.strptime(end_date.value, "%Y-%m-%d")
                else:
                    end = end_date.value

                date_diff = end - start

                if date_diff.days > 31:
                    new_end_date = (start + timedelta(days=31))
                    end_date.value = new_end_date.strftime("%Y-%m-%d")
                    page.update()
                    print("El rango de fechas no puede ser mayor a un mes")
                elif date_diff.days < 0:
                    end_date.value = start_date.value if isinstance(start_date.value, str) else start_date.value.strftime("%Y-%m-%d")
                    page.update()
                    print("La fecha final no puede ser menor que la inicial")
            except Exception as e:
                print(f"Error en validate_date_range: {str(e)}")

    # Variables para el texto de los botones
    start_date_text = ft.Text("Desde la fecha", color="#1a73e8", size=14, weight=ft.FontWeight.W_500)
    end_date_text = ft.Text("Hasta la fecha", color="#1a73e8", size=14, weight=ft.FontWeight.W_500)

    def update_date_button_text(e, is_start_date=True):
        if e.control.value:
            try:
                # Convertir a datetime si es string
                if isinstance(e.control.value, str):
                    date_obj = datetime.strptime(e.control.value, "%Y-%m-%d")
                else:
                    date_obj = e.control.value
                    
                formatted_date = date_obj.strftime("%d/%m/%Y")
                if is_start_date:
                    start_date_text.value = f"Desde: {formatted_date}"
                else:
                    end_date_text.value = f"Hasta: {formatted_date}"
                page.update()
            except Exception as e:
                print(f"Error en update_date_button_text: {str(e)}")

    # Actualizar los DatePicker con la validación y actualización de texto
    start_date.on_change = lambda e: [update_date_button_text(e, True), validate_date_range()]
    end_date.on_change = lambda e: [update_date_button_text(e, False), validate_date_range()]

    # Crear botones personalizados para mostrar los DatePicker
    start_date_button = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.icons.CALENDAR_TODAY, color="#1a73e8"),
                start_date_text,
            ],
            spacing=8,
        ),
        padding=ft.padding.all(10),
        border=ft.border.all(1, "#1a73e8"),
        border_radius=8,
        ink=True,
        on_click=lambda _: start_date.pick_date(),
        bgcolor="#ffffff"
    )
    
    end_date_button = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.icons.CALENDAR_TODAY, color="#1a73e8"),
                end_date_text,
            ],
            spacing=8,
        ),
        padding=ft.padding.all(10),
        border=ft.border.all(1, "#1a73e8"),
        border_radius=8,
        ink=True,
        on_click=lambda _: end_date.pick_date(),
        bgcolor="#ffffff"
    )

    # Crear un selector para los autoreportes
    report_selector = ft.Dropdown(
        label="Seleccionar reporte",
        options=[
            ft.dropdown.Option("Autoreportes de salud"),
            ft.dropdown.Option("Chequeos de limpieza"),
            ft.dropdown.Option("Preoperacionales"),
        ],
        value="Autoreportes de salud",
        border_radius=8,
        text_size=14,
        label_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
        focused_border_color="#1a73e8",
        focused_color="#1a73e8",
    )

    # Botón de filtrar
    filter_button = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.icons.FILTER_ALT, color="#ffffff"),
                ft.Text("Filtrar", color="#ffffff", size=14, weight=ft.FontWeight.W_500),
            ],
            spacing=8,
        ),
        padding=ft.padding.all(10),
        bgcolor="#1a73e8",
        border_radius=8,
        ink=True,
        on_click=lambda e: filter_data(start_date.value, end_date.value, report_selector.value),
    )

    # Crear un contenedor para los componentes de filtro
    filter_controls = ft.Container(
        content=ft.Row(
            controls=[
                start_date_button,
                end_date_button,
                report_selector,
                filter_button
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=16,
        ),
        padding=ft.padding.all(16),
        bgcolor="#ffffff",
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.1, "#000000"),
            offset=ft.Offset(0, 2),
        )
    )

    data_table_column = ft.Column()

    def filter_data(start_date_obj, end_date_obj, report_type):
        if start_date_obj and end_date_obj:
            try:
                if isinstance(start_date_obj, str):
                    start = datetime.strptime(start_date_obj, "%Y-%m-%d")
                else:
                    start = start_date_obj
                
                if isinstance(end_date_obj, str):
                    end = datetime.strptime(end_date_obj, "%Y-%m-%d")
                else:
                    end = end_date_obj
                
                start = start.replace(hour=0, minute=0, second=0)
                end = end.replace(hour=23, minute=59, second=59)
                
                reports = report_controller.get_filtered_reports(start, end, report_type)
                data_table = create_data_table(reports)
                data_table_column.controls.clear()
                data_table_column.controls.append(data_table)
                page.update()
            except Exception as e:
                print(f"Error en filter_data: {str(e)}")

    page.add(start_date, end_date)  

    # Layout principal
    page.add(ft.Row(controls=[sidebar, ft.Column(controls=[filter_controls, data_table_column])]))

if __name__ == "__main__":
    ft.app(target=main)