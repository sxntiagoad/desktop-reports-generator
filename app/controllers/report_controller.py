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
                # Convertir las cadenas de fecha a objetos datetime
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
            
            if isinstance(end_date_str, datetime):
                end_date = end_date_str
            else:
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
            
            # Crear el filtro
            filter = ReportFilter(
                start_date=start_date,
                end_date=end_date,
                report_type=report_type
            )
            
            # Obtener los reportes
            return self.repository.get_reports(filter)
            
        except ValueError as e:
            print(f"Error processing filter: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return []
