"""
Controlador principal - Homepage y rutas generales
Aplicación de escritorio local (sin autenticación)
"""

from flask import Blueprint, render_template, session

main_bp = Blueprint('main', __name__)

# ID de usuario local fijo (aplicación de escritorio)
LOCAL_USER_ID = 1
LOCAL_USERNAME = "Usuario"


def init_local_session():
    """Inicializa la sesión para el usuario local."""
    if 'user_id' not in session:
        session['user_id'] = LOCAL_USER_ID
        session['username'] = LOCAL_USERNAME


@main_bp.before_app_request
def before_request():
    """Se ejecuta antes de cada request para asegurar la sesión local."""
    init_local_session()


@main_bp.route('/')
def index():
    """Página principal - redirige directamente al dashboard."""
    return render_template('dashboard.html')


@main_bp.route('/dashboard')
def dashboard():
    """Dashboard principal con gráficas."""
    return render_template('dashboard.html')


@main_bp.route('/health')
def health_check():
    """Endpoint de salud para verificar que la aplicación está corriendo."""
    return {'status': 'healthy', 'app': 'GymGraph'}
