import os
import flet as ft
from datetime import datetime, timedelta
from app.controllers.report_controller import ReportController
from app.presentation.widgets.data_table import create_data_table
from app.config.firebase_config import db

def main(page: ft.Page):
    report_controller = ReportController()
    current_reports = []  # Variable para mantener los reportes actuales

    global kits_list, projects_list, vehicles_list
    kits_list = []
    projects_list = []
    vehicles_list = []
    # Cargar datos de Firebase
    doc = db.collection('typekid').document('kyb0aLSQnumHGvPKkIT1').get()
    if doc.exists:
        kits_list = doc.to_dict().get('kids',[])

    doc1 = db.collection('proyectos').document('list_proyectos').get()
    if doc1.exists:
        projects_list = doc1.to_dict().get('proyectos',[])
    doc_cars = db.collection('cars').get()
    
    # Configuración inicial de la página
    page.title = "Merchants Dashboard"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#f8f9fa"

    # Crear DatePickers
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

    # Agregar DatePickers a la página primero
    page.overlay.extend([start_date, end_date])

    # Sidebar mejorado
    sidebar = ft.Container(
        width=250,
        bgcolor="#1e293b",
        padding=20,
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.DASHBOARD, color="white"),
                            ft.Text("Dashboard", color="white", size=16, weight=ft.FontWeight.W_500),
                        ],
                        spacing=10,
                    ),
                    padding=10,
                    border_radius=8,
                    ink=True,
                    on_click=lambda _: print("Dashboard clicked"),
                ),
                ft.Divider(color="white24", height=30),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.ASSESSMENT, color="white"),
                            ft.Text("Reportes", color="white", size=16),
                        ],
                        spacing=10,
                    ),
                    padding=10,
                    border_radius=8,
                    ink=True,
                    on_click=lambda _: print("Reportes clicked"),
                ),
            ],
        ),
    )

    # Indicador de progreso
    progress_indicator = ft.ProgressRing(visible=False)  # Inicialmente oculto

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
        border_radius=8,
        text_size=14,
        label_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
        focused_border_color="#1a73e8",
        focused_color="#1a73e8",
    )

    vehicle_selector = ft.Dropdown(
        label="Seleccionar vehículo(Opcional)",
        options=[
            ft.dropdown.Option("Vehículo 1"),
            ft.dropdown.Option("Vehículo 2"),
            ft.dropdown.Option("Vehículo 3"),
        ],
        border_radius=8,
        text_size=14,
        label_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
        focused_border_color="#1a73e8",
        focused_color="#1a73e8",
        visible=False  # Inicialmente oculto
    )

    project_selector = ft.Dropdown(
        label="Seleccionar proyecto (Opcional)",
        options=[
            ft.dropdown.Option("Todos", None),  # Opción que devuelve None
            *[ft.dropdown.Option(kid) for kid in kits_list]
        ],
        border_radius=8,
        text_size=14,
        label_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
        focused_border_color="#1a73e8",
        focused_color="#1a73e8",
        hint_text="Seleccione o escoja Todos",
        visible=False
    )

    def on_report_type_change(e):
        selected_value = e.control.value
        if selected_value == "Preoperacionales":
            vehicle_selector.visible = True
            project_selector.visible = True
            project_selector.options = [
                ft.dropdown.Option("Todos", None),  # Opción que devuelve None
                *[ft.dropdown.Option(kid) for kid in kits_list]
            ]
        elif selected_value == "Autoreportes de salud":
            vehicle_selector.visible = False
            project_selector.visible = True
            project_selector.options = [
                ft.dropdown.Option("Todos", None),  # Opción que devuelve None
                *[ft.dropdown.Option(proyecto) for proyecto in projects_list]
            ]
        elif selected_value == "Chequeos de limpieza":
            vehicle_selector.visible = True
            project_selector.visible = False
        
        project_selector.value = None
        page.update()
    # Asignar el callback al report_selector
    report_selector.on_change = on_report_type_change

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
                ft.Row(
                    controls=[
                        start_date_button,
                        end_date_button,
                        report_selector,
                        vehicle_selector,    # Agregar nuevo selector
                        project_selector,   # Agregar nuevo selector
                    ],
                    spacing=16,
                ),
                filter_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
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

    # Crear un overlay de carga más elegante
    loading_overlay = ft.Container(
        content=ft.Column(
            controls=[
                ft.ProgressRing(
                    width=40,
                    height=40,
                    stroke_width=3,
                    color="#1a73e8",
                ),
                ft.Container(height=20),  # Espaciador
                ft.Text(
                    "Cargando datos...",
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color="#1a73e8",
                ),
                ft.Text(
                    "Por favor espere",
                    size=14,
                    color="#666666",
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=ft.colors.with_opacity(0.9, "#ffffff"),
        padding=40,
        border_radius=12,
        visible=False,
    )

    # Contenedor para la tabla de datos con el overlay de carga
    data_table_container = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=create_data_table(),
                            expand=True,
                            alignment=ft.alignment.top_center,
                        ),
                    ],
                    expand=True,
                ),
                ft.Row(
                    controls=[loading_overlay],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
            ],
        ),
        padding=16,
        bgcolor="white",
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.with_opacity(0.1, "#000000"),
            offset=ft.Offset(0, 2),
        ),
    )

    # Layout principal mejorado
    content_area = ft.Container(
        content=ft.Column(
            controls=[
                filter_controls,
                ft.Container(height=16),  # Espaciador
                data_table_container
            ],
            expand=True,  # Expandir la columna principal
            spacing=0,
        ),
        padding=16,
        expand=True,  # Expandir el contenedor principal
    )

    # Layout principal con Row expandible
    main_row = ft.Row(
        controls=[
            sidebar,
            ft.VerticalDivider(width=1, color="#EEEEEE"),
            content_area
        ],
        expand=True,
        spacing=0,
    )

    # Configuración de la página
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#f8f9fa"
    
    # Agregar el layout principal a la página
    page.add(main_row)

    # Función para manejar cambios en el tamaño de la ventana
    def page_resize(e):
        # Ajustar el sidebar si la ventana es muy pequeña
        if page.window_width < 600:
            sidebar.width = 60
            # Ocultar texto en el sidebar
            for control in sidebar.content.controls:
                if isinstance(control, ft.Container):
                    control.content.controls = [control.content.controls[0]]  # Solo mantener el icono
        else:
            sidebar.width = 250
            # Mostrar texto en el sidebar
            # Aquí puedes restaurar el texto si lo necesitas
        page.update()

    # Suscribirse al evento de cambio de tamaño de la ventana
    page.on_resize = page_resize

    # Actualizar la página
    page.update()

    def handle_row_movement(direction, index):
        nonlocal current_reports
        try:
            index = int(index) - 1
            if direction == "up" and index > 0:
                current_reports[index], current_reports[index-1] = current_reports[index-1], current_reports[index]
            elif direction == "down" and index < len(current_reports) - 1:
                current_reports[index], current_reports[index+1] = current_reports[index+1], current_reports[index]
            
            # Actualizar los índices
            for i, report in enumerate(current_reports, 1):
                report['index'] = i
            
            # Actualizar la tabla asegurando pasar el callback
            new_table = create_data_table(
                current_reports, 
                handle_row_movement,
                handle_file_click,
                handle_delete
            )
            data_table_container.content.controls[0].controls[0].content = new_table
            page.update()
            
        except Exception as e:
            print(f"Error al mover fila: {str(e)}")

    def handle_file_click(pdf_path):
        """Maneja el clic en un archivo PDF."""
        if pdf_path and os.path.exists(pdf_path):
            try:
                # En Windows, esto abrirá el PDF con el visor predeterminado
                os.startfile(pdf_path)
            except Exception as e:
                print(f"Error al abrir el PDF: {str(e)}")

    def handle_delete(index):
        """Maneja la eliminación de una fila"""
        nonlocal current_reports
        try:
            index = int(index) - 1
            if 0 <= index < len(current_reports):
                # Eliminar el reporte
                deleted_report = current_reports.pop(index)
                print(f"Reporte eliminado: {deleted_report.get('doc_id')}")
                
                # Reindexar los reportes restantes
                for i, report in enumerate(current_reports, 1):
                    report['index'] = i
                
                # Actualizar la tabla
                new_table = create_data_table(
                    current_reports,
                    handle_row_movement,
                    handle_file_click,
                    handle_delete
                )
                data_table_container.content.controls[0].controls[0].content = new_table
                page.update()
        except Exception as e:
            print(f"Error al eliminar fila: {str(e)}")

    def filter_data(start_date_obj, end_date_obj, report_type):
        nonlocal current_reports
        if start_date_obj and end_date_obj:
            try:
                loading_overlay.visible = True
                page.update()

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
                # Obtener los valores opcionales
                project = None if project_selector.value == "Todos" else project_selector.value
                car = None if vehicle_selector.value== "Todos" else vehicle_selector.value
                print(project)
                print(car)
                # Agregar los valores opcionales al filtro
                current_reports = report_controller.get_filtered_reports(
                    start, 
                    end, 
                    report_type,
                    project=project,  # Parámetro opcional de proyecto
                    car=car  # Parámetro opcional de vehículo
                )
                
                # Asegurarse de que cada reporte tenga un índice
                for i, report in enumerate(current_reports, 1):
                    report['index'] = i
                new_table = create_data_table(
                    current_reports, 
                    handle_row_movement,
                    handle_file_click,
                    handle_delete
                )
                data_table_container.content.controls[0].controls[0].content = new_table
                
                # Iniciar el procesamiento de PDFs
                def on_reports_updated(updated_reports):
                    nonlocal current_reports
                    current_reports = updated_reports
                    new_table = create_data_table(
                        current_reports, 
                        handle_row_movement,
                        handle_file_click,
                        handle_delete
                    )
                    data_table_container.content.controls[0].controls[0].content = new_table
                    page.update()
                
                # Iniciar procesamiento en segundo plano
                report_controller.process_reports_to_pdf(current_reports, on_reports_updated)
                
            except Exception as e:
                print(f"Error en filter_data: {str(e)}")
            finally:
                loading_overlay.visible = False
                page.update()

if __name__ == "__main__":
    ft.app(target=main)