import os
from PyPDF2 import PdfMerger
import tempfile

def combine_pdfs(pdf_paths, output_filename="combined_reports.pdf"):
    """Combina múltiples PDFs en uno solo."""
    try:
        print(f"Iniciando combinación de PDFs. Paths recibidos: {pdf_paths}")
        merger = PdfMerger()
        
        # Verificar que todos los archivos existan y sean accesibles
        valid_paths = [path for path in pdf_paths if path and os.path.exists(path)]
        print(f"Paths válidos encontrados: {valid_paths}")
        
        if not valid_paths:
            print("No se encontraron PDFs válidos para combinar")
            raise Exception("No hay PDFs válidos para combinar")
            
        # Agregar cada PDF al merger
        for pdf_path in valid_paths:
            print(f"Agregando PDF: {pdf_path}")
            merger.append(pdf_path)
            
        # Crear el archivo combinado en el directorio temporal
        temp_dir = os.path.join(tempfile.gettempdir(), 'eva_reports_temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        output_path = os.path.join(temp_dir, output_filename)
        print(f"Guardando PDF combinado en: {output_path}")
        merger.write(output_path)
        merger.close()
        
        print(f"PDF combinado creado exitosamente en: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error al combinar PDFs: {str(e)}")
        return None

if __name__ == "__main__":
    pdf_paths = [
        r"C:\Users\Santiago\AppData\Local\Temp\eva_reports_temp\wLTAOzDJYeT4TGUMdmgN.pdf",
        r"C:\Users\Santiago\AppData\Local\Temp\eva_reports_temp\JHsgM2plsWoz9618hB7l.pdf",
        r"C:\Users\Santiago\AppData\Local\Temp\eva_reports_temp\nqolQtgAeSkKbyv0zkTI.pdf",
        r"C:\Users\Santiago\AppData\Local\Temp\eva_reports_temp\vuOD2DTwAN1gEb7CanyX.pdf",
        r"C:\Users\Santiago\AppData\Local\Temp\eva_reports_temp\VTWgVhMYz6Ibvq7qV2Ep.pdf"
    ]
    output_path = combine_pdfs(pdf_paths)
    if output_path:
        os.startfile(output_path)  # Abre el archivo combinado con el visualizador predeterminado