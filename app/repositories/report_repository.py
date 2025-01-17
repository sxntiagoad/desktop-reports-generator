import os
from threading import Thread
from typing import Any, Dict, List
from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from google.cloud.firestore_v1.types import StructuredQuery
from app.config.firebase_config import db, bucket
from app.models.report_filter import ReportFilter
from datetime import datetime
import tempfile
from concurrent.futures import ThreadPoolExecutor
import time

from app.utils.excel_converter import convert_excel_to_pdf

class ReportRepository:
    def __init__(self):
        # Crear un directorio temporal específico para nuestra aplicación
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'eva_reports_temp')
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def __del__(self):
        """Limpia los archivos temporales al destruir la instancia"""
        try:
            if os.path.exists(self.temp_dir):
                for file in os.listdir(self.temp_dir):
                    file_path = os.path.join(self.temp_dir, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Error eliminando {file_path}: {e}")
                os.rmdir(self.temp_dir)
        except Exception as e:
            print(f"Error limpiando directorio temporal: {e}")

    def get_reports(self, report_filter: ReportFilter) -> List[Dict[str, Any]]:
        try:
            # Mapear tipos de reporte a colecciones
            collection_map = {
                "Autoreportes de salud": "autoreportes",
                "Chequeos de limpieza": "limpiezas",
                "Preoperacionales": "preoperacionales"
            }
            
            collection = collection_map.get(report_filter.report_type, "preoperacionales")
            collection_ref = db.collection(collection)
            
            # Agregar collection_type a los resultados
            collection_type = collection
            
            if report_filter.collection == 'preoperacionales':
                start_date_filter = FieldFilter('fechaInit', '>=', report_filter.start_date)
                end_date_filter = FieldFilter('fechaInit', '<=', report_filter.end_date)
            else:
                start_date_filter = FieldFilter('fecha', '>=', report_filter.start_date)
                end_date_filter = FieldFilter('fecha', '<=', report_filter.end_date)
            
            composite_filter = BaseCompositeFilter(
                StructuredQuery.CompositeFilter.Operator.AND, 
                [start_date_filter, end_date_filter]
            )
            if report_filter.collection == 'preoperacionales':
                query = collection_ref.where(filter=composite_filter).select(['userId', 'fechaInit' , 'carId', 'typeKit'])  # Solo cargar userId y fechaInit
                docs = query.get()
            elif report_filter.collection == 'limpieza':
                query = collection_ref.where(filter=composite_filter).select(['userId', 'fecha' , 'carId'])  # Solo cargar userId y fechaInit
                docs = query.get()
            else:
                query = collection_ref.where(filter=composite_filter).select(['userId', 'fecha' , 'carId', 'selectedValue'])  # Solo cargar userId y fechaInit
                docs = query.get()

            # Procesar documentos con índice
            results = []
            for index, doc in enumerate(docs, 1):  # Empezar índice en 1
                data = doc.to_dict()
                if report_filter.collection == 'preoperacionales':
                    data.update({
                        'collection_type': collection_type,  # Agregar collection_type
                        'index': index,
                        'doc_id': doc.id,  # ID del documento
                        'fecha_formatted': datetime.strptime(data.get('fechaInit', ''),"%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M"),
                        'user_uid': data.get('userId', ''),
                        'user_name': self.fetch_name(data.get('userId', ''), 'users', 'fullName'),
                        'car_plate': self.fetch_name(data.get('carId', ''), 'cars', 'carPlate'),
                        'project': data.get('typeKit', ''),
                        'pdf_path': None,
                        'processing_status': 'pending'
                    })
                    results.append(data)
                elif report_filter.collection == 'limpiezas':
                    data.update({
                        'collection_type': collection_type,  # Agregar collection_type
                        'index': index,
                        'doc_id': doc.id,  # ID del documento
                        'fecha_formatted': datetime.strptime(data.get('fechaInit', ''),"%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M"),
                        'user_uid': data.get('userId', ''),
                        'user_name': self.fetch_name(data.get('userId', ''), 'users', 'fullName'),
                        'car_plate': self.fetch_name(data.get('carId', ''), 'cars', 'carPlate'),
                        'project': data.get('selectedValue', ''),
                        'pdf_path': None,
                        'processing_status': 'pending'
                    })
                    results.append(data)
                else:
                    data.update({
                        'collection_type': collection_type,  # Agregar collection_type
                        'index': index,
                        'doc_id': doc.id,  # ID del documento
                        'fecha_formatted': datetime.strptime(data.get('fecha', ''),"%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M"),
                        'user_uid': data.get('userId', ''),
                        'user_name': self.fetch_name(data.get('userId', ''), 'users', 'fullName'),
                        'pdf_path': None,
                        'processing_status': 'pending'
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

    def process_report_to_pdf(self, bucket_collection: str, reports: List[Dict[str, Any]], callback=None):
        MAX_WORKERS = 2
        MAX_RETRIES = 3
        RETRY_DELAY = 2

        def process_single_report(report):
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    doc_id = report['doc_id']
                    
                    report['processing_status'] = 'processing'
                    if callback: callback(reports)

                    # Crear paths temporales específicos
                    temp_excel_path = os.path.join(self.temp_dir, f"{doc_id}.xlsx")
                    pdf_path = os.path.join(self.temp_dir, f"{doc_id}.pdf")
                    
                    # Si el PDF ya existe y es accesible, usarlo
                    if os.path.exists(pdf_path):
                        try:
                            with open(pdf_path, 'rb') as f:
                                f.read(1)
                            report['pdf_path'] = pdf_path
                            report['processing_status'] = 'completed'
                            if callback: callback(reports)
                            return
                        except:
                            print(f"PDF existente pero no accesible para {doc_id}")
                            try:
                                os.remove(pdf_path)
                            except:
                                pass

                    # Procesar el reporte
                    try:
                        excel_blob = bucket.blob(f"{bucket_collection}/{doc_id}.xlsx")
                        excel_blob.download_to_filename(temp_excel_path)
                        result_pdf_path = convert_excel_to_pdf(temp_excel_path)

                        if result_pdf_path and os.path.exists(result_pdf_path):
                            report['pdf_path'] = result_pdf_path
                            report['processing_status'] = 'completed'
                            break
                        else:
                            raise Exception("PDF no generado")

                    finally:
                        if os.path.exists(temp_excel_path):
                            try:
                                os.unlink(temp_excel_path)
                            except:
                                pass

                except Exception as e:
                    print(f"Error procesando {doc_id} (intento {retries + 1}): {str(e)}")
                    retries += 1
                    if retries < MAX_RETRIES:
                        time.sleep(RETRY_DELAY)
                        report['processing_status'] = 'retrying'
                    else:
                        report['processing_status'] = 'error'
                    if callback: callback(reports)

        # Procesar los reportes
        reports_to_process = [r for r in reports if r.get('processing_status') != 'completed']
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []
            for report in reports_to_process:
                future = executor.submit(process_single_report, report)
                futures.append(future)
            
            # Esperar a que todos terminen
            for future in futures:
                try:
                    future.result(timeout=5)
                except Exception as e:
                    print(f"Error en el procesamiento: {str(e)}")

            # Verificar si quedó alguno pendiente y volver a procesar
            pending_reports = [r for r in reports if r.get('processing_status') in ['pending', 'error']]
            if pending_reports:
                for report in pending_reports:
                    try:
                        process_single_report(report)
                    except Exception as e:
                        print(f"Error en el reprocesamiento: {str(e)}")

            # Actualizar UI una última vez
            if callback: 
                print("Actualizando UI final")
                callback(reports)