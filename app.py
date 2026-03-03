# app.py - PUNTO DE ENTRADA (solo configuración)
import os
from flask import Flask
from flask_login import LoginManager
from controllers import CurrentUser
from database import get_db

# Crear la app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """Carga usuario desde BD para Flask-Login"""
    from repositories.user_repository import UserRepository
    repo = UserRepository()
    with get_db() as db:
        user = repo.get_by_id(db, int(user_id))
        return CurrentUser(user) if user else None
   

# Registrar blueprints (controladores)
from controllers.auth_controller import auth_bp
app.register_blueprint(auth_bp)

from controllers.macros_controller import macros_bp
app.register_blueprint(macros_bp)

from controllers.food_controller import food_bp
app.register_blueprint(food_bp)

from controllers.train_controller import train_bp
app.register_blueprint(train_bp)

from controllers.dashboard_controller import dashboard_bp
app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(debug=True)