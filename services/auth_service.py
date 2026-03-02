# services/auth_service.py
from werkzeug.security import generate_password_hash, check_password_hash
from repositories.user_repository import UserRepository
from database import get_db

class AuthService:
    """Lógica de negocio para autenticación"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def signup(self, username, password):
        """
        Registrar nuevo usuario
        Retorna: dict con success, user/error
        """
        # 1. Validaciones básicas
        if not username or not password:
            return {
                'success': False, 
                'error': 'Usuario y contraseña son obligatorios'
            }
        
        if len(password) < 3:
            return {
                'success': False, 
                'error': 'La contraseña debe tener al menos 3 caracteres'
            }
        
        # 2. Usar contexto de BD
        with get_db() as db:
            # Verificar si ya existe
            if self.user_repo.username_exists(db, username):
                return {
                    'success': False, 
                    'error': 'El nombre de usuario ya está registrado'
                }
            
            # Crear usuario con contraseña hasheada
            try:
                hashed = generate_password_hash(password)
                user = self.user_repo.create(db, username, hashed)
                
                return {
                    'success': True,
                    'user': user,
                    'message': 'Registro exitoso'
                }
            except Exception as e:
                # Log del error (en producción usa logging)
                print(f"Error en signup: {e}")
                return {
                    'success': False,
                    'error': 'Error al crear el usuario'
                }
    
    def login(self, username, password):
        """
        Autenticar usuario
        Retorna: dict con success, user/error
        """
        # Validaciones básicas
        if not username or not password:
            return {
                'success': False, 
                'error': 'Usuario y contraseña son obligatorios'
            }
        
        with get_db() as db:
            # Buscar usuario
            user = self.user_repo.get_by_username(db, username)
            
            if not user:
                return {
                    'success': False, 
                    'error': 'Usuario o contraseña incorrectos'
                }
            
            # Verificar contraseña
            if check_password_hash(user.passwd, password):

                user_data = {
                    'id': user.idUser,
                    'username': user.username
                }

                return {
                    'success': True,
                    'user_data': user_data,
                    'message': 'Login exitoso'
                }
            else:
                return {
                    'success': False, 
                    'error': 'Usuario o contraseña incorrectos'
                }