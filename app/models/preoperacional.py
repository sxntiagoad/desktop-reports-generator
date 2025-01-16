from datetime import datetime
from app.config.firebase_config import db

class Preoperacional:
    def __init__(self, doc_id: str, fecha_init: str, user_id: str, index: int):
        self.doc_id = doc_id
        self.fecha_init = fecha_init
        self.user_id = user_id
        self.index = index
        self.full_name = self.fetch_full_name,

    def set_full_name(self, full_name: str):
        self.full_name = full_name
    
    def fetch_full_name(self):
        """Obtiene el nombre completo del usuario desde Firestore."""
        try:
            user_doc = db.collection('users').document(self.user_uid).get()
            if user_doc.exists:
                self.full_name = user_doc.to_dict().get('fullName', '')
            else:
                self.full_name = ''
        except Exception as e:
            print(f"Error al obtener el nombre del usuario: {str(e)}")
            self.full_name = ''
    