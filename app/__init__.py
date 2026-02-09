"""
GymGraph - Aplicación de seguimiento fitness integral
Autores: Huilin Jin, Arkaitz Cambra, Andrés Salamanca
"""

import os
import sys
from flask import Flask
from flask_cors import CORS
from config import Config


def get_resource_path(relative_path):
    """
    Obtiene la ruta correcta del recurso, funciona tanto con PyInstaller como en desarrollo.
    """
    if getattr(sys, 'frozen', False):
        # Si está empaquetado con PyInstaller
        base_path = sys._MEIPASS
    else:
        # Si está en desarrollo
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)


def create_app(config_class=Config):
    """Factory de la aplicación Flask."""
    # Obtener rutas correctas para templates y static
    template_dir = get_resource_path('templates')
    static_dir = get_resource_path('static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    app.config.from_object(config_class)
    
    CORS(app)
    
    CORS(app)
    
    # Registrar blueprints
    from app.controllers.main_controller import main_bp
    from app.controllers.workout_controller import workout_bp
    from app.controllers.nutrition_controller import nutrition_bp
    from app.controllers.measurement_controller import measurement_bp
    from app.controllers.selfcare_controller import selfcare_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.charts_controller import charts_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(workout_bp, url_prefix='/workout')
    app.register_blueprint(nutrition_bp, url_prefix='/nutrition')
    app.register_blueprint(measurement_bp, url_prefix='/measurement')
    app.register_blueprint(selfcare_bp, url_prefix='/selfcare')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(charts_bp, url_prefix='/charts')
    
    return app
