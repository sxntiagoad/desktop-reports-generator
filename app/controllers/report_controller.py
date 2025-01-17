from datetime import datetime
from typing import List, Dict, Any
from app.models.report_filter import ReportFilter
from app.repositories.report_repository import ReportRepository

class ReportController:
    def __init__(self):
        self.repository = ReportRepository()
    
    def get_filtered_reports(self, start_date_str: str, end_date_str: str, report_type: str) -> List[Dict[str, Any]]:
        try:
            # Verificar si las fechas son objetos datetime
            if isinstance(start_date_str, datetime):
                start_date = start_date_str
            else:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
            
            if isinstance(end_date_str, datetime):
                end_date = end_date_str
            else:
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
            
            # Crear el filtro
            filter = ReportFilter(
                report_type=report_type,
                start_date=start_date,
                end_date=end_date
            )
            
            # Obtener los reportes
            return self.repository.get_reports(filter)
            
        except Exception as e:
            print(f"Error en get_filtered_reports: {str(e)}")
            return []

    def process_reports_to_pdf(self, reports: List[Dict[str, Any]], callback=None):
        if not reports:
            return []
            
        collection_type = reports[0].get('collection_type', 'preoperacionales')
        return self.repository.process_report_to_pdf(collection_type, reports, callback)
