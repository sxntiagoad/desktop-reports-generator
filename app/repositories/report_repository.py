from typing import Any, Dict, List
from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from google.cloud.firestore_v1.types import StructuredQuery
from app.config.firebase_config import db
from app.models.report_filter import ReportFilter

class ReportRepository:
    def get_reports(self, report_filter: ReportFilter) -> List[Dict[str, Any]]:
        try:
            print("Iniciando get_reports...")
            collection_ref = db.collection(report_filter.collection)
            
            # Crear filtros individuales
            start_date_filter = FieldFilter('fechaInit', '>=', report_filter.start_date)
            end_date_filter = FieldFilter('fechaInit', '<=', report_filter.end_date)
            
            composite_filter = BaseCompositeFilter(
                StructuredQuery.CompositeFilter.Operator.AND, 
                [start_date_filter, end_date_filter]
            )

            # Aplicar filtro a la consulta
            query = collection_ref.where(filter=composite_filter)
            docs = query.get()

            # Extraer datos e IDs
            results = []
            for doc in docs:
                data = doc.to_dict()
                data['doc_id'] = doc.id  # Agregar el ID del documento al diccionario
                results.append(data)
            
            print(f"Procesados {len(results)} documentos")
            return results
            
        except Exception as e:
            print(f"Error en la consulta: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            import traceback
            print(f"Stacktrace: {traceback.format_exc()}")
            return []
