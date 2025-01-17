from datetime import datetime
from typing import Optional

class ReportFilter:
    REPORT_COLLECTIONS = {
        "Autoreportes de salud": "health_reports",
        "Chequeos de limpieza": "limpieza",
        "Preoperacionales": "preoperacionales"
    }

    def __init__(self, start_date: Optional[datetime] = None, 
                 end_date: Optional[datetime] = None, 
                 report_type: str = "Preoperacionales",
                 project: Optional[str] = None,
                 car: Optional[str] = None):
        if start_date and isinstance(start_date, datetime):
            self.start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.start_date = None
            
        if end_date and isinstance(end_date, datetime):
            self.end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.end_date = None
            
        self.report_type = report_type
        self.collection = self.REPORT_COLLECTIONS.get(report_type)
        self.project = project
        self.car = car

    @property 
    def collection_name(self) -> str:
        return self.collection
    
    def is_valid(self) -> bool:
        if not all([self.start_date, self.end_date]):
            return False
        start = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
        return start <= end
    
    def date_range_in_days(self) -> Optional[int]:
        if not self.is_valid():
            return None
        start = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
        return (end - start).days