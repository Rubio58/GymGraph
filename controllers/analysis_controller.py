"""
Controlador para análisis de datos: correlaciones, métricas por tiempo, etc.
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from services.analysis_service import AnalysisService

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/api/analysis/metrics', methods=['GET'])
@login_required
def get_available_metrics():
    """Lista todas las métricas disponibles"""
    service = AnalysisService()
    metrics = service.get_available_metrics()
    service.close()
    return jsonify(metrics)


@analysis_bp.route('/api/analysis/metric-data', methods=['GET'])
@login_required
def get_metric_data():
    """Obtiene datos de una métrica en un rango de tiempo"""
    metric = request.args.get('metric', 'calories')
    days = request.args.get('days', '30', type=int)

    service = AnalysisService()
    data = service.get_metric_data(current_user.idUser, metric, days)
    service.close()

    return jsonify(data)


@analysis_bp.route('/api/analysis/correlation', methods=['GET'])
@login_required
def calculate_correlation():
    """Calcula la correlación de Pearson entre dos métricas"""
    metric1 = request.args.get('metric1')
    metric2 = request.args.get('metric2')
    days = request.args.get('days', '30', type=int)

    if not metric1 or not metric2:
        return jsonify({'error': 'Se requieren metric1 y metric2'}), 400

    service = AnalysisService()
    result = service.calculate_correlation(current_user.idUser, metric1, metric2, days)
    service.close()

    return jsonify(result)
