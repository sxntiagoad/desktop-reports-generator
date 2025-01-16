import flet as ft
from typing import Any, List, Dict

def create_data_table(reports: List[Dict[str, Any]] = None) -> ft.Container:
    # Tabla vacía si no hay reportes
    if reports is None:
        reports = []
        
    table = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Container(
                    ft.Text("#", text_align=ft.TextAlign.CENTER),
                    width=50,  # Ancho fijo para la columna numérica
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
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(report.get('index', '')), text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ft.Text(report.get('fecha_formatted', ''), text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ft.Text(report.get('user_name', ''), text_align=ft.TextAlign.CENTER)),
                    ft.DataCell(ft.Text(report.get('car_plate', ''), text_align=ft.TextAlign.CENTER))
                ]
            ) for report in reports
        ],
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