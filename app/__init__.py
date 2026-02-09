"""
GymGraph - Aplicación de seguimiento fitness integral
Autores: Huilin Jin, Arkaitz Cambra, Andrés Salamanca
"""

from flask import Flask
from flask_cors import CORS
from config import Config


def create_app(config_class=Config):
    """Factory de la aplicación Flask."""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config_class)
    
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
