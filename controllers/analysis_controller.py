"""
Controlador para análisis de datos: correlaciones, métricas por tiempo, etc.
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from services.analysis_service import AnalysisService
from datetime import date as date_cls, timedelta

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')


@analysis_bp.route('/metrics', methods=['GET'])
@login_required
def get_available_metrics():
    """Lista todas las métricas disponibles"""
    service = AnalysisService()
    metrics = service.get_available_metrics(user_id=current_user.id)
    service.close()
    return jsonify(metrics)


@analysis_bp.route('/metric-data', methods=['GET'])
@login_required
def get_metric_data():
    """Obtiene datos de una métrica en un rango de tiempo"""
    metric = request.args.get('metric', 'calories')
    all_time = request.args.get('all_time') == 'true'
    days = request.args.get('days', 30, type=int)
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')

    end_date = date_cls.fromisoformat(end_str) if end_str else date_cls.today()
    start_date = date_cls.fromisoformat(start_str) if start_str else None

    service = AnalysisService()
    data = service.get_metric_data(current_user.id, metric, days,
                                   start_date=start_date, end_date=end_date,
                                   all_time=all_time)
    service.close()

    return jsonify(data)


@analysis_bp.route('/correlation', methods=['GET'])
@login_required
def calculate_correlation():
    """Calcula la correlación de Pearson entre dos métricas"""
    metric1 = request.args.get('metric1')
    metric2 = request.args.get('metric2')
    days = request.args.get('days', 30, type=int)
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')

    if not metric1 or not metric2:
        return jsonify({'error': 'Se requieren metric1 y metric2'}), 400

    all_time = request.args.get('all_time') == 'true'
    end_date = date_cls.fromisoformat(end_str) if end_str else date_cls.today()
    start_date = date_cls.fromisoformat(start_str) if start_str else None

    service = AnalysisService()
    result = service.calculate_correlation(current_user.id, metric1, metric2, days,
                                           start_date=start_date, end_date=end_date,
                                           all_time=all_time)
    service.close()

    return jsonify(result)
