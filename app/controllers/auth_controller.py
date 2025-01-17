from app.models.user import CurrentUser
from app.config.firebase_config import auth_client, auth, db

class AuthController:
    def __init__(self):
        self.current_user = CurrentUser()

    def login(self, email, password):
        try:
            # Autenticar usuario con Pyrebase
            user = auth_client.sign_in_with_email_and_password(email, password)
            
            # Obtener información adicional del usuario
            user_info = auth.get_user_by_email(email)
            
            # Obtener datos adicionales del usuario desde Firestore
            user_doc = db.collection("users").document(user_info.uid).get()
            
            if user_doc.exists:
                user_data = user_doc.to_dict()
                # Actualizar el CurrentUser con la información
                self.current_user.login(
                    user_id=user_info.uid,
                    email=user_info.email,
                    name=user_data.get("fullName", user_info.email),
                    role=user_data.get("role", "CONDUCTOR")
                )
            
            # Imprimir los datos del usuario
            print("Inicio de sesión exitoso:")
            print(f"ID de usuario: {self.current_user.user_id}")
            print(f"Email: {self.current_user.email}")
            print(f"Nombre: {self.current_user.name}")
            print(f"Rol: {self.current_user.role}")
            print(f"Autenticado: {self.current_user.is_authenticated}")
            
            return self.current_user
            
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return None

    def logout(self):
        try:
            # Cerrar sesión en Firebase
            auth_client.current_user = None
            
            # Limpiar y destruir la instancia del usuario actual
            self.current_user.logout()
            
            return True
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")
            return False