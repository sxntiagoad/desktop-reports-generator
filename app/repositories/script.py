from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from google.cloud.firestore_v1.types import StructuredQuery
from google.cloud import firestore
from app.config.firebase_config import db



def fetch_preoperacionales():
    try:
        # Referencia a la colección
        collection_ref = db.collection("preoperacionales")

        # Crear filtros
        fecha_final_filter = FieldFilter("fechaFinal", "==", "2024-11-27 08:54:39")
        kilometraje_init_filter = FieldFilter("kilometrajeInit", "==", 471033)
        is_open_filter = FieldFilter("isOpen", "==", False)

        # Crear filtro compuesto con "AND"
        composite_filter = BaseCompositeFilter(
            StructuredQuery.CompositeFilter.Operator.AND,
            [fecha_final_filter, kilometraje_init_filter, is_open_filter]
        )

        # Aplicar filtro a la consulta
        query = collection_ref.where(filter=composite_filter)

        # Ejecutar la consulta
        docs = query.get()

        # Imprimir resultados
        results = [doc.to_dict() for doc in docs]
        for result in results:
            print(result)

        return results

    except Exception as e:
        print(f"Error al ejecutar la consulta: {str(e)}")
        return []

# Ejecutar el script
if __name__ == "__main__":
    fetch_preoperacionales()