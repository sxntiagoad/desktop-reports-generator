import os
import win32com.client
import pythoncom
import time

def convert_excel_to_pdf(input_excel_path):
    """
    Convierte un archivo Excel específico a PDF.
    
    Args:
        input_excel_path (str): Ruta completa al archivo Excel a convertir
        
    Returns:
        str: Ruta del archivo PDF generado o None si hay error
    """
    excel = None
    wb = None
    
    try:
        # Inicializar COM para el hilo actual
        pythoncom.CoInitialize()
        
        # Generar la ruta de salida del PDF
        output_pdf_path = os.path.join(
            os.path.dirname(input_excel_path),
            f"{os.path.splitext(os.path.basename(input_excel_path))[0]}.pdf"
        )
        
        # Iniciar Excel con un timeout
        for _ in range(3):  # Intentar 3 veces
            try:
                excel = win32com.client.Dispatch("Excel.Application")
                excel.Visible = False
                excel.DisplayAlerts = False
                break
            except Exception:
                time.sleep(2)  # Esperar 2 segundos antes de reintentar
                continue
        
        if excel is None:
            raise Exception("No se pudo iniciar Excel después de 3 intentos")

        # Abrir el archivo Excel
        wb = excel.Workbooks.Open(input_excel_path)
        ws = wb.Worksheets[0]
        
        # Configurar área de impresión y ajustes
        ws.PageSetup.PrintArea = "A1:U85"
        ws.PageSetup.FitToPagesWide = 1
        ws.PageSetup.FitToPagesTall = 2
        ws.PageSetup.Orientation = 1  # xlPortrait
        ws.PageSetup.PaperSize = 9   # A4
        ws.PageSetup.LeftMargin = excel.InchesToPoints(0.75)
        ws.PageSetup.RightMargin = excel.InchesToPoints(0.75)
        ws.PageSetup.TopMargin = excel.InchesToPoints(0.75)
        ws.PageSetup.BottomMargin = excel.InchesToPoints(0.75)
        
        # Ajustar el zoom
        ws.PageSetup.Zoom = 44
        
        # Exportar a PDF con timeout
        for _ in range(3):  # Intentar 3 veces
            try:
                wb.ExportAsFixedFormat(0, output_pdf_path)
                if os.path.exists(output_pdf_path):
                    break
            except Exception:
                time.sleep(2)
                continue
        
        return output_pdf_path if os.path.exists(output_pdf_path) else None
        
    except Exception as e:
        print(f"Error en la conversión de Excel a PDF: {str(e)}")
        return None
        
    finally:
        try:
            if wb is not None:
                wb.Close(False)
            if excel is not None:
                excel.Quit()
                excel = None
        except:
            pass
        finally:
            pythoncom.CoUninitialize()

if __name__ == "__main__":
    # Ejemplo de uso directo del script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivos_excel = [archivo for archivo in os.listdir(directorio_actual) 
                     if archivo.endswith(('.xlsx', '.xls'))]
    
    if archivos_excel:
        archivo_excel = archivos_excel[0]
        input_path = os.path.join(directorio_actual, archivo_excel)
        pdf_path = convert_excel_to_pdf(input_path)
        
        if pdf_path:
            print(f"PDF generado exitosamente en: {pdf_path}")
    else:
        print("No se encontró ningún archivo Excel en el directorio.")