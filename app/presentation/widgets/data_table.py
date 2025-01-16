import flet as ft
from typing import Any, List, Dict

def create_data_table(reports: List[Dict[str, Any]] = None, on_row_select=None) -> ft.Container:
    # Tabla vacía si no hay reportes
    if reports is None:
        reports = []
        
    # Agregar botones de control para mover filas
    controls_column = ft.DataColumn(
        ft.Container(
            ft.Text("Controles", text_align=ft.TextAlign.CENTER),
            width=70,
            alignment=ft.alignment.center,
        ),
    )
    
    # Insertar la columna de controles al inicio
    columns = [controls_column] + [
        ft.DataColumn(
            ft.Container(
                ft.Text("#", text_align=ft.TextAlign.CENTER),
                width=10,  # Ancho fijo para la columna numérica
                alignment=ft.alignment.center,
            ),
            numeric=True,
        ),
        ft.DataColumn(
            ft.Container(
                ft.Text("Fecha", text_align=ft.TextAlign.CENTER),
                expand=True,
                width=200,  # Ancho mínimo
                alignment=ft.alignment.center,
            ),
        ),
        ft.DataColumn(
            ft.Container(
                ft.Text("Usuario", text_align=ft.TextAlign.CENTER),
                expand=True,
                width=200,  # Ancho mínimo
                alignment=ft.alignment.center,
            ),
        ),
        ft.DataColumn(
            ft.Container(
                ft.Text("Placa del Vehículo", text_align=ft.TextAlign.CENTER),
                expand=True,
                width=200,  # Ancho mínimo
                alignment=ft.alignment.center,
            ),
        ),
        ft.DataColumn(
            ft.Container(
                ft.Text("Proyecto de la operación", text_align=ft.TextAlign.CENTER),
                expand=True,
                width=200,  # Ancho mínimo
                alignment=ft.alignment.center,
            ),
        ),
    ]
    
    def create_row_controls(index):
        return ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_UPWARD,
                    icon_size=20,
                    tooltip="Mover arriba",
                    on_click=lambda e, idx=index: on_row_select("up", idx) if on_row_select else None,
                ),
                ft.IconButton(
                    icon=ft.icons.ARROW_DOWNWARD,
                    icon_size=20,
                    tooltip="Mover abajo",
                    on_click=lambda e, idx=index: on_row_select("down", idx) if on_row_select else None,
                ),
            ],
            spacing=0,
        )
    
    # Modificar la creación de filas para incluir los controles
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(create_row_controls(report.get('index', ''))),  # Columna de controles
                ft.DataCell(ft.Text(str(report.get('index', '')), text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(report.get('fecha_formatted', ''), text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(report.get('user_name', ''), text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(report.get('car_plate', ''), text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(report.get('project', ''), text_align=ft.TextAlign.CENTER))
            ]
        ) for report in reports
    ]
    
    table = ft.DataTable(
        columns=columns,
        rows=rows,
        border=ft.border.all(1, "#EEEEEE"),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, "#EEEEEE"),
        horizontal_lines=ft.border.BorderSide(1, "#EEEEEE"),
        heading_row_height=70,  # Altura del encabezado
        data_row_min_height=30,  # Altura mínima de las filas
        data_row_max_height=50,  # Altura máxima de las filas
        column_spacing=70,  # Quitamos el spacing fijo
        expand=True,
    )
    
    return ft.Container(
        content=ft.Column(
            controls=[table],
            scroll=ft.ScrollMode.ALWAYS,
        ),
        height=800,  # Altura fija del contenedor
        border_radius=8,
        expand=True,
    ) 