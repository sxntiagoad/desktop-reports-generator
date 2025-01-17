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
            
            if not report_filter.start_date or not report_filter.end_date:
                print("Error: Fechas de filtro inválidas")
                return []
            
            collection = report_filter.collection
            if not collection:
                print("Error: Colección no especificada")
                return []
            
            collection_ref = db.collection(collection)
            
            # Lista para almacenar todos los filtros
            filters = []
            
            # Agregar filtros de fecha según la colección
            if collection == 'preoperacionales':
                filters.append(FieldFilter('fechaInit', '>=', report_filter.start_date))
                filters.append(FieldFilter('fechaInit', '<=', report_filter.end_date))
            elif collection == 'limpieza':
                # Para la colección de limpieza, verificar que el campo fecha no esté vacío
                filters.append(FieldFilter('fecha', '>=', report_filter.start_date))
                filters.append(FieldFilter('fecha', '<=', report_filter.end_date))
            else:  # health-reports y otros
                filters.append(FieldFilter('fecha', '>=', report_filter.start_date))
                filters.append(FieldFilter('fecha', '<=', report_filter.end_date))
            
            # Agregar filtro de vehículo si existe
            if report_filter.car:
                car_id = self.fetch_car_id_by_plate(report_filter.car)
                if car_id:  # Solo agregar si se encontró el ID del vehículo
                    filters.append(FieldFilter('carId', '==', car_id))
            
            # Agregar filtro de proyecto si existe
            if report_filter.project:
                if collection == 'preoperacionales':
                    filters.append(FieldFilter('typeKit', '==', report_filter.project))
                else:
                    filters.append(FieldFilter('selectedValue', '==', report_filter.project))
            
            # Crear el filtro compuesto con todos los filtros
            composite_filter = BaseCompositeFilter(
                StructuredQuery.CompositeFilter.Operator.AND, 
                filters
            )

            # Aplicar el filtro compuesto a la consulta y seleccionar campos específicos
            if collection == 'preoperacionales':
                query = collection_ref.where(filter=composite_filter).select(['userId', 'fechaInit', 'carId', 'typeKit'])
            elif collection == 'limpieza':
                query = collection_ref.where(filter=composite_filter).select(['userId', 'fecha', 'carId'])
            else:  # health-reports
                query = collection_ref.where(filter=composite_filter).select(['userId', 'fecha', 'carId', 'selectedValue'])

            docs = query.get()
            
            # Procesar documentos con índice
            results = []
            for index, doc in enumerate(docs, 1):
                try:
                    data = doc.to_dict()
                    if not data:
                        continue
                    
                    # Verificar y formatear la fecha según el tipo de colección
                    fecha = None
                    if collection == 'preoperacionales':
                        fecha = data.get('fechaInit', '')
                    else:
                        fecha = data.get('fecha', '')
                    
                    if not fecha:  # Saltar documentos sin fecha
                        continue
                        
                    try:
                        fecha_formatted = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
                    except ValueError:
                        continue  # Saltar documentos con formato de fecha inválido
                    # Construir el diccionario de resultados base
                    result = {
                        'collection_type': collection,
                        'index': index,
                        'doc_id': doc.id,
                        'fecha_formatted': fecha_formatted,
                        'user_uid': data.get('userId', ''),
                        'user_name': self.fetch_name(data.get('userId', ''), 'users', 'fullName'),
                        'pdf_path': None,
                        'processing_status': 'pending'
                    }
                    
                    # Agregar campos específicos según el tipo de colección
                    if collection in ['preoperacionales', 'limpieza']:
                        result['car_plate'] = self.fetch_name(data.get('carId', ''), 'cars', 'carPlate')
                    
                    if collection in ['preoperacionales', 'health_reports']:
                        result['project'] = data.get('typeKit' if collection == 'preoperacionales' else 'selectedValue', '')
                    
                    results.append(result)
                    
                except Exception as e:
                    print(f"Error procesando documento {doc.id}: {str(e)}")
                    continue
            
            print(f"Procesados {len(results)} documentos")
            return results
            
        except Exception as e:
            print(f"Error en la consulta: {str(e)}")
            return []
        

    def fetch_car_id_by_plate(self, car_plate: str) -> str:
        try:
            car_doc = db.collection('cars').where('carPlate', '==', car_plate).get()
            return car_doc[0].id
        except Exception as e:
            print(f"Error al obtener el ID del vehículo: {str(e)}")
            return None

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

        # Mapeo de colecciones a rutas de Storage
        STORAGE_PATHS = {
            'health_reports': 'reportes_salud',
            'limpieza': 'chequeos_limpieza',
            'preoperacionales': 'preoperacionales'
        }

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
                    storage_path = STORAGE_PATHS.get(bucket_collection, 'preoperacionales')                
                    # Procesar el reporte según su tipo
                    try:
                        excel_blob = bucket.blob(f"{storage_path}/{doc_id}.xlsx")
                        excel_blob.download_to_filename(temp_excel_path)
                    
                        # Seleccionar el script de conversión según el tipo de reporte
                        if bucket_collection == 'preoperacionales':
                            result_pdf_path = convert_excel_to_pdf(temp_excel_path, script='preoperacionales')
                        elif bucket_collection == 'health_reports':
                            result_pdf_path = convert_excel_to_pdf(temp_excel_path, script='health-reports')
                        elif bucket_collection == 'limpieza':
                            result_pdf_path = convert_excel_to_pdf(temp_excel_path, script='limpieza')
                        else:
                            raise Exception(f"Tipo de reporte no soportado: {bucket_collection}")

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
            pending_reports = [r for r in reports if r.get('processing_status') in ['pending', 'error', 'retrying']]
            
            if pending_reports:
                for report in pending_reports:
                    try:
                        process_single_report(report)
                    except Exception as e:
                        print(f"Error en el reprocesamiento: {str(e)}")

            # Reprocesar todos los reportes una última vez para asegurar
            final_check_reports = [r for r in reports if r.get('processing_status') != 'completed']
            if final_check_reports:
                print("Realizando verificación final de reportes...")
                for report in final_check_reports:
                    try:
                        process_single_report(report)
                    except Exception as e:
                        print(f"Error en la verificación final: {str(e)}")
            # Actualizar UI una última vez
            if callback: 
                print("Actualizando UI final")
                callback(reports)