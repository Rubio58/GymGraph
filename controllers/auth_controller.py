# controllers/auth_controller.py
from types import SimpleNamespace
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from controllers import CurrentUser
from services.auth_service import AuthService

# Crear blueprint para agrupar rutas de autenticación
auth_bp = Blueprint('auth', __name__)

# ========== RUTAS PÚBLICAS ==========
@auth_bp.route('/')
def index():
    """Redirige a login"""
    return redirect(url_for('auth.login'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Registro de usuarios"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Delegar al servicio
        service = AuthService()
        result = service.signup(username, password)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(result['error'], 'error')
            return redirect(url_for('auth.signup'))
    
    return render_template('auth/signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        service = AuthService()
        result = service.login(request.form['username'], request.form['password'])
        
        if result['success']:

            user_data=result['user_data']
            user_obj=SimpleNamespace(idUser=user_data['id'],username=user_data['username'])
            user=CurrentUser(user_obj)
            login_user(user, remember=True)
            flash('Login exitoso!', 'success')
            return redirect(url_for('auth.dashboard')) 
        else:
            flash(result['error'], 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Página principal después del login"""
    return render_template('dashboard.html')
