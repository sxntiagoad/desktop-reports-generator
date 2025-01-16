import flet as ft
from typing import Any, List, Dict

def create_data_table(data: List[Dict[str, Any]]) -> ft.DataTable:
    # Definir las columnas de la tabla
    columns = [
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Email")),
        ft.DataColumn(ft.Text("Ubicación")),
        ft.DataColumn(ft.Text("Estado")),
        ft.DataColumn(ft.Text("Título del Trabajo")),
        ft.DataColumn(ft.Text("Universidad")),
    ]

    # Crear las filas de la tabla
    rows = []
    for item in data:
        rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(item.get("name", ""))),
            ft.DataCell(ft.Text(item.get("email", ""))),
            ft.DataCell(ft.Text(item.get("location", ""))),
            ft.DataCell(ft.Text(item.get("status", ""))),
            ft.DataCell(ft.Text(item.get("job_title", ""))),
            ft.DataCell(ft.Text(item.get("university", ""))),
        ]))

    # Crear la tabla
    data_table = ft.DataTable(
        columns=columns,
        rows=rows,
        border=ft.border.all(1, "#ccc"),
        border_radius=8,
        bgcolor="#ffffff",
    )

    return data_table 