import flet as ft
from typing import Any, List, Dict
import os

def create_data_table(reports: List[Dict[str, Any]] = None, on_row_select=None, on_file_click=None, on_delete=None) -> ft.Container:
    # Tabla vacía si no hay reportes
    if reports is None:
        reports = []
    
    # Obtener collection_type del primer reporte si existe
    collection_type = reports[0].get('collection_type') if reports else None
    
    # Agregar botones de control para mover filas
    controls_column = ft.DataColumn(
        ft.Container(
            ft.Text("Controles", text_align=ft.TextAlign.CENTER),
            width=70,
            alignment=ft.alignment.center,
        ),
    )
    
    # Definir columnas base
    base_columns = [
        controls_column,
        ft.DataColumn(
            ft.Container(
                ft.Text("#", text_align=ft.TextAlign.CENTER),
                width=50,
                alignment=ft.alignment.center,
            ),
        ),
        ft.DataColumn(
            ft.Container(
                ft.Text("Fecha", text_align=ft.TextAlign.CENTER),
                width=200,
                alignment=ft.alignment.center,
            ),
        ),
        ft.DataColumn(
            ft.Container(
                ft.Text("Usuario", text_align=ft.TextAlign.CENTER),
                width=200,
                alignment=ft.alignment.center,
            ),
        ),
        ft.DataColumn(
            ft.Container(
                ft.Text("PDF", text_align=ft.TextAlign.CENTER),
                width=70,
                alignment=ft.alignment.center,
            ),
        ),
    ]
    
    # Agregar columnas específicas según el tipo de colección
    if collection_type in ['preoperacionales', 'limpiezas']:
        additional_columns = [
            ft.DataColumn(
                ft.Container(
                    ft.Text("Placa del Vehículo", text_align=ft.TextAlign.CENTER),
                    width=200,
                    alignment=ft.alignment.center,
                ),
            ),
            ft.DataColumn(
                ft.Container(
                    ft.Text("Proyecto", text_align=ft.TextAlign.CENTER),
                    width=200,
                    alignment=ft.alignment.center,
                ),
            ),
        ]
        base_columns.extend(additional_columns)
    
    columns = base_columns

    def create_row_controls(index):
        """Crea los controles de movimiento y eliminación para cada fila"""
        return ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_UPWARD,
                    icon_color="blue",
                    icon_size=20,
                    tooltip="Mover arriba",
                    on_click=lambda e, idx=index: handle_row_movement("up", idx)
                ),
                ft.IconButton(
                    icon=ft.icons.ARROW_DOWNWARD,
                    icon_color="blue",
                    icon_size=20,
                    tooltip="Mover abajo",
                    on_click=lambda e, idx=index: handle_row_movement("down", idx)
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color="red",
                    icon_size=20,
                    tooltip="Eliminar",
                    on_click=lambda e, idx=index: handle_delete(idx)
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        )
    
    def handle_row_movement(direction, index):
        if on_row_select:
            # Guardar el estado actual de los PDFs
            pdf_states = {report['doc_id']: {
                'pdf_path': report.get('pdf_path'),
                'processing_status': report.get('processing_status')
            } for report in reports}
            
            # Llamar al callback de movimiento
            on_row_select(direction, index)
            
            # Restaurar el estado de los PDFs después del movimiento
            for report in reports:
                if report['doc_id'] in pdf_states:
                    report['pdf_path'] = pdf_states[report['doc_id']]['pdf_path']
                    report['processing_status'] = pdf_states[report['doc_id']]['processing_status']

    def handle_delete(index):
        """Maneja la eliminación de una fila"""
        if on_delete:
            on_delete(index)

    def get_file_button(report):
        status = report.get('processing_status', 'pending')
        pdf_path = report.get('pdf_path')
        
        print(f"Estado del botón PDF - ID: {report.get('doc_id')} - Status: {status} - Path: {pdf_path}")
        
        if status == 'pending':
            return ft.IconButton(
                icon=ft.icons.FILE_PRESENT,
                icon_color="grey",
                tooltip="Pendiente de procesar"
            )
        elif status == 'processing' or status == 'retrying':
            return ft.ProgressRing(width=20, height=20)
        elif status == 'completed':
            if pdf_path and os.path.exists(pdf_path):
                return ft.IconButton(
                    icon=ft.icons.PICTURE_AS_PDF,
                    icon_color="green",
                    tooltip="Ver PDF",
                    on_click=lambda e, path=pdf_path: handle_pdf_click(path)
                )
            else:
                print(f"PDF no encontrado - Path: {pdf_path}")
                return ft.IconButton(
                    icon=ft.icons.ERROR,
                    icon_color="red",
                    tooltip="PDF no encontrado"
                )
        else:  # error
            return ft.IconButton(
                icon=ft.icons.ERROR,
                icon_color="red",
                tooltip="Error en el procesamiento"
            )

    def handle_pdf_click(pdf_path):
        try:
            print(f"Intentando abrir PDF: {pdf_path}")
            if os.path.exists(pdf_path):
                on_file_click(pdf_path)
            else:
                print(f"Error: El archivo PDF no existe en la ruta: {pdf_path}")
        except Exception as e:
            print(f"Error al abrir el PDF: {str(e)}")
    
    # Modificar la creación de filas para incluir el botón de archivo
    def create_row_cells(report):
        # Asegurarnos de que el pdf_path se mantenga después de mover la fila
        if report.get('processing_status') == 'completed' and report.get('pdf_path'):
            if not os.path.exists(report['pdf_path']):
                report['processing_status'] = 'error'
                report['pdf_path'] = None

        base_cells = [
            ft.DataCell(create_row_controls(report.get('index', ''))),
            ft.DataCell(ft.Text(str(report.get('index', '')), text_align=ft.TextAlign.CENTER)),
            ft.DataCell(ft.Text(report.get('fecha_formatted', ''), text_align=ft.TextAlign.CENTER)),
            ft.DataCell(ft.Text(report.get('user_name', ''), text_align=ft.TextAlign.CENTER)),
            ft.DataCell(get_file_button(report))
        ]
        
        if collection_type in ['preoperacionales', 'limpiezas']:
            additional_cells = [
                ft.DataCell(ft.Text(report.get('car_plate', ''), text_align=ft.TextAlign.CENTER)),
                ft.DataCell(ft.Text(report.get('project', ''), text_align=ft.TextAlign.CENTER))
            ]
            base_cells.extend(additional_cells)
            
        return base_cells
    
    rows = [ft.DataRow(cells=create_row_cells(report)) for report in reports]
    
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
