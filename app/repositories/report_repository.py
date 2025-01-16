from typing import Any, Dict, List
from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from google.cloud.firestore_v1.types import StructuredQuery
from app.config.firebase_config import db
from app.models.report_filter import ReportFilter
from datetime import datetime

class ReportRepository:
    def get_reports(self, report_filter: ReportFilter) -> List[Dict[str, Any]]:
        try:
            collection_ref = db.collection(report_filter.collection)
            
            # Crear filtros individuales
            start_date_filter = FieldFilter('fechaInit', '>=', report_filter.start_date)
            end_date_filter = FieldFilter('fechaInit', '<=', report_filter.end_date)
            
            composite_filter = BaseCompositeFilter(
                StructuredQuery.CompositeFilter.Operator.AND, 
                [start_date_filter, end_date_filter]
            )

            query = collection_ref.where(filter=composite_filter).select(['userId', 'fechaInit' , 'carId'])  # Solo cargar userId y fechaInit
            docs = query.get()

            # Procesar documentos con índice
            results = []
            for index, doc in enumerate(docs, 1):  # Empezar índice en 1
                data = doc.to_dict()
                data.update({
                    'index': index,  # Añadir índice para la tabla
                    'doc_id': doc.id,  # ID del documento
                    'fecha_formatted': datetime.strptime(data.get('fechaInit', ''), 
                                                       "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M"),
                    'user_uid': data.get('userId', ''),
                    'user_name': self.fetch_name(data.get('userId', ''), 'users', 'fullName'),
                    'car_plate': self.fetch_name(data.get('carId', ''), 'cars', 'carPlate')
                })
                results.append(data)
            
            print(f"Procesados {len(results)} documentos")
            return results
            
        except Exception as e:
            print(f"Error en la consulta: {str(e)}")
            return []
        
    def fetch_name(self, doc_uid: str, collection: str, field: str):
        """Obtiene el nombre completo del usuario desde Firestore."""
        try:
            user_doc = db.collection(collection).document(doc_uid).get()
            if user_doc.exists:
                name = user_doc.to_dict().get(field, '')
            else:
                name = ''
            return name
        except Exception as e:
            print(f"Error al obtener el nombre del usuario: {str(e)}")
            name = ''
            return name
    
