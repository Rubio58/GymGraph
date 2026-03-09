# controllers/dashboard_controller.py
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard_api', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/macros')
@login_required
def macros_chart():
    """Datos de macros de los últimos 7 días"""
    service = DashboardService()
    data = service.get_macros_last_days(current_user.id, days=7)
    return jsonify(data)

@dashboard_bp.route('/weight-progress')
@login_required
def weight_progress():
    """Evolución del peso por ejercicio"""
    service = DashboardService()
    data = service.get_weight_progress(current_user.id)
    return jsonify(data)

@dashboard_bp.route('/muscle-distribution')
@login_required
def muscle_distribution():
    """Distribución por grupo muscular"""
    service = DashboardService()
    data = service.get_muscle_distribution(current_user.id)
    return jsonify(data)

@dashboard_bp.route('/volume')
@login_required
def volume():
    """Volumen por sesión"""
    service = DashboardService()
    data = service.get_volume_per_session(current_user.id)
    return jsonify(data)

@dashboard_bp.route('/today-macros')
@login_required
def today_macros():
    """Macros de hoy vs objetivo"""
    service = DashboardService()
    data = service.get_today_macros_vs_objective(current_user.id)
    return jsonify(data)

@dashboard_bp.route('/last-workout')
@login_required
def last_workout():
    """Datos del último entrenamiento"""
    service = DashboardService()
    data = service.get_last_workout(current_user.id)
    return jsonify(data)
