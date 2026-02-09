"""
Controlador de Gráficas y Análisis
Permite visualizar y correlacionar cualquier métrica en el tiempo
"""

from flask import Blueprint, render_template, session, jsonify, request
from datetime import date, datetime, timedelta
from app.models.database import Database

charts_bp = Blueprint('charts', __name__)


@charts_bp.route('/')
def index():
    """Vista principal de gráficas."""
    return render_template('charts/index.html')


@charts_bp.route('/api/metrics')
def get_available_metrics():
    """Devuelve la lista de métricas disponibles para graficar."""
    # Paleta retro-moderna cálida
    metrics = [
        # Nutrición
        {'id': 'calories', 'name': 'Calorías', 'category': 'Nutrición', 'unit': 'kcal', 'color': '#C67B5C'},  # terracotta
        {'id': 'protein', 'name': 'Proteína', 'category': 'Nutrición', 'unit': 'g', 'color': '#6B7B8C'},      # slate-blue
        {'id': 'carbs', 'name': 'Carbohidratos', 'category': 'Nutrición', 'unit': 'g', 'color': '#E8D4A8'},   # soft-yellow
        {'id': 'fat', 'name': 'Grasas', 'category': 'Nutrición', 'unit': 'g', 'color': '#D4956C'},            # muted-orange
        {'id': 'water', 'name': 'Agua', 'category': 'Nutrición', 'unit': 'L', 'color': '#8C9DAD'},            # dusty-blue
        
        # Medidas corporales
        {'id': 'weight', 'name': 'Peso', 'category': 'Medidas', 'unit': 'kg', 'color': '#8FA584'},            # sage
        {'id': 'body_fat', 'name': '% Grasa corporal', 'category': 'Medidas', 'unit': '%', 'color': '#B85C4C'}, # brick
        {'id': 'chest', 'name': 'Pecho', 'category': 'Medidas', 'unit': 'cm', 'color': '#A5B5C5'},            # soft-blue
        {'id': 'waist', 'name': 'Cintura', 'category': 'Medidas', 'unit': 'cm', 'color': '#CC8860'},          # warm-orange
        {'id': 'hips', 'name': 'Cadera', 'category': 'Medidas', 'unit': 'cm', 'color': '#7C8C6C'},            # olive
        {'id': 'biceps', 'name': 'Bíceps (media)', 'category': 'Medidas', 'unit': 'cm', 'color': '#9E5A4C'},  # rust
        {'id': 'thighs', 'name': 'Muslos (media)', 'category': 'Medidas', 'unit': 'cm', 'color': '#A85D42'},  # terracotta-dark
        
        # Autocuidado
        {'id': 'sleep_hours', 'name': 'Horas de sueño', 'category': 'Autocuidado', 'unit': 'h', 'color': '#6B7B8C'},   # slate-blue
        {'id': 'sleep_quality', 'name': 'Calidad de sueño', 'category': 'Autocuidado', 'unit': '/10', 'color': '#8C9DAD'}, # dusty-blue
        {'id': 'steps', 'name': 'Pasos', 'category': 'Autocuidado', 'unit': 'pasos', 'color': '#8FA584'},     # sage
        
        # Entrenamiento
        {'id': 'workout_volume', 'name': 'Volumen total (peso x reps)', 'category': 'Entrenamiento', 'unit': 'kg', 'color': '#B85C4C'},  # brick
        {'id': 'workout_sets', 'name': 'Series totales', 'category': 'Entrenamiento', 'unit': 'series', 'color': '#A5B5C5'},  # soft-blue
        {'id': 'workout_duration', 'name': 'Duración entrenamientos', 'category': 'Entrenamiento', 'unit': 'min', 'color': '#7C8C6C'},  # olive
    ]
    return jsonify(metrics)


@charts_bp.route('/api/data')
def get_metric_data():
    """
    Obtiene datos de una o más métricas.
    Query params:
        - metrics: lista de IDs de métricas separadas por coma
        - start_date: fecha inicio (YYYY-MM-DD)
        - end_date: fecha fin (YYYY-MM-DD)
    """
    user_id = session.get('user_id', 1)
    
    metrics_param = request.args.get('metrics', '')
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())
    
    if not metrics_param:
        return jsonify({'error': 'No metrics specified'}), 400
    
    metric_ids = [m.strip() for m in metrics_param.split(',')]
    
    result = {}
    for metric_id in metric_ids:
        data = get_metric_values(user_id, metric_id, start_date, end_date)
        result[metric_id] = data
    
    return jsonify(result)


def get_metric_values(user_id, metric_id, start_date, end_date):
    """Obtiene los valores de una métrica específica."""
    
    queries = {
        # Nutrición - agregados diarios
        'calories': """
            SELECT fl.log_date as date, 
                   SUM(f.calories * fl.quantity) as value
            FROM food_logs fl
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = ? AND fl.log_date BETWEEN ? AND ?
            GROUP BY fl.log_date
            ORDER BY fl.log_date
        """,
        'protein': """
            SELECT fl.log_date as date,
                   SUM(f.protein_g * fl.quantity) as value
            FROM food_logs fl
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = ? AND fl.log_date BETWEEN ? AND ?
            GROUP BY fl.log_date
            ORDER BY fl.log_date
        """,
        'carbs': """
            SELECT fl.log_date as date,
                   SUM(f.carbs_g * fl.quantity) as value
            FROM food_logs fl
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = ? AND fl.log_date BETWEEN ? AND ?
            GROUP BY fl.log_date
            ORDER BY fl.log_date
        """,
        'fat': """
            SELECT fl.log_date as date,
                   SUM(f.fat_g * fl.quantity) as value
            FROM food_logs fl
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = ? AND fl.log_date BETWEEN ? AND ?
            GROUP BY fl.log_date
            ORDER BY fl.log_date
        """,
        'water': """
            SELECT log_date as date, liters as value
            FROM water_logs
            WHERE user_id = ? AND log_date BETWEEN ? AND ?
            ORDER BY log_date
        """,
        
        # Medidas corporales
        'weight': """
            SELECT measurement_date as date, weight_kg as value
            FROM body_measurements
            WHERE user_id = ? AND measurement_date BETWEEN ? AND ?
            AND weight_kg IS NOT NULL
            ORDER BY measurement_date
        """,
        'body_fat': """
            SELECT measurement_date as date, body_fat_percentage as value
            FROM body_measurements
            WHERE user_id = ? AND measurement_date BETWEEN ? AND ?
            AND body_fat_percentage IS NOT NULL
            ORDER BY measurement_date
        """,
        'chest': """
            SELECT measurement_date as date, chest_cm as value
            FROM body_measurements
            WHERE user_id = ? AND measurement_date BETWEEN ? AND ?
            AND chest_cm IS NOT NULL
            ORDER BY measurement_date
        """,
        'waist': """
            SELECT measurement_date as date, waist_cm as value
            FROM body_measurements
            WHERE user_id = ? AND measurement_date BETWEEN ? AND ?
            AND waist_cm IS NOT NULL
            ORDER BY measurement_date
        """,
        'hips': """
            SELECT measurement_date as date, hips_cm as value
            FROM body_measurements
            WHERE user_id = ? AND measurement_date BETWEEN ? AND ?
            AND hips_cm IS NOT NULL
            ORDER BY measurement_date
        """,
        'biceps': """
            SELECT measurement_date as date, 
                   (COALESCE(bicep_left_cm, 0) + COALESCE(bicep_right_cm, 0)) / 2.0 as value
            FROM body_measurements
            WHERE user_id = ? AND measurement_date BETWEEN ? AND ?
            AND (bicep_left_cm IS NOT NULL OR bicep_right_cm IS NOT NULL)
            ORDER BY measurement_date
        """,
        'thighs': """
            SELECT measurement_date as date,
                   (COALESCE(thigh_left_cm, 0) + COALESCE(thigh_right_cm, 0)) / 2.0 as value
            FROM body_measurements
            WHERE user_id = ? AND measurement_date BETWEEN ? AND ?
            AND (thigh_left_cm IS NOT NULL OR thigh_right_cm IS NOT NULL)
            ORDER BY measurement_date
        """,
        
        # Autocuidado
        'sleep_hours': """
            SELECT log_date as date, hours_slept as value
            FROM sleep_logs
            WHERE user_id = ? AND log_date BETWEEN ? AND ?
            ORDER BY log_date
        """,
        'sleep_quality': """
            SELECT log_date as date, sleep_quality as value
            FROM sleep_logs
            WHERE user_id = ? AND log_date BETWEEN ? AND ?
            AND sleep_quality IS NOT NULL
            ORDER BY log_date
        """,
        'steps': """
            SELECT log_date as date, steps as value
            FROM step_logs
            WHERE user_id = ? AND log_date BETWEEN ? AND ?
            ORDER BY log_date
        """,
        
        # Entrenamiento
        'workout_volume': """
            SELECT ws.session_date as date,
                   SUM(wset.weight_kg * wset.reps) as value
            FROM workout_sessions ws
            JOIN workout_sets wset ON ws.id = wset.session_id
            WHERE ws.user_id = ? AND ws.session_date BETWEEN ? AND ?
            GROUP BY ws.session_date
            ORDER BY ws.session_date
        """,
        'workout_sets': """
            SELECT ws.session_date as date,
                   COUNT(wset.id) as value
            FROM workout_sessions ws
            JOIN workout_sets wset ON ws.id = wset.session_id
            WHERE ws.user_id = ? AND ws.session_date BETWEEN ? AND ?
            GROUP BY ws.session_date
            ORDER BY ws.session_date
        """,
        'workout_duration': """
            SELECT session_date as date,
                   (strftime('%s', end_time) - strftime('%s', start_time)) / 60.0 as value
            FROM workout_sessions
            WHERE user_id = ? AND session_date BETWEEN ? AND ?
            AND start_time IS NOT NULL AND end_time IS NOT NULL
            ORDER BY session_date
        """,
    }
    
    if metric_id not in queries:
        return []
    
    results = Database.execute_query(queries[metric_id], (user_id, start_date, end_date))
    
    # Formatear resultados
    formatted = []
    for row in results:
        if row['value'] is not None:
            formatted.append({
                'date': str(row['date']),
                'value': round(float(row['value']), 2) if row['value'] else 0
            })
    
    return formatted


@charts_bp.route('/api/correlation')
def calculate_correlation():
    """
    Calcula la correlación de Pearson entre dos métricas.
    Query params:
        - metric1: ID de la primera métrica
        - metric2: ID de la segunda métrica
        - start_date, end_date: rango de fechas
    """
    user_id = session.get('user_id', 1)
    
    metric1 = request.args.get('metric1')
    metric2 = request.args.get('metric2')
    start_date = request.args.get('start_date', (date.today() - timedelta(days=90)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())
    
    if not metric1 or not metric2:
        return jsonify({'error': 'Se requieren dos métricas'}), 400
    
    # Obtener datos de ambas métricas
    data1 = get_metric_values(user_id, metric1, start_date, end_date)
    data2 = get_metric_values(user_id, metric2, start_date, end_date)
    
    # Crear diccionarios por fecha
    dict1 = {d['date']: d['value'] for d in data1}
    dict2 = {d['date']: d['value'] for d in data2}
    
    # Encontrar fechas comunes
    common_dates = set(dict1.keys()) & set(dict2.keys())
    
    if len(common_dates) < 3:
        return jsonify({
            'correlation': None,
            'message': 'No hay suficientes datos coincidentes para calcular correlación (mínimo 3 puntos)',
            'common_points': len(common_dates)
        })
    
    # Extraer valores para fechas comunes
    values1 = [dict1[d] for d in sorted(common_dates)]
    values2 = [dict2[d] for d in sorted(common_dates)]
    
    # Calcular correlación de Pearson
    correlation = pearson_correlation(values1, values2)
    
    # Interpretar la correlación
    interpretation = interpret_correlation(correlation)
    
    return jsonify({
        'correlation': round(correlation, 4),
        'interpretation': interpretation,
        'common_points': len(common_dates),
        'scatter_data': [
            {'x': v1, 'y': v2, 'date': d} 
            for d, v1, v2 in zip(sorted(common_dates), values1, values2)
        ]
    })


def pearson_correlation(x, y):
    """Calcula el coeficiente de correlación de Pearson."""
    n = len(x)
    if n == 0:
        return 0
    
    # Medias
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    # Desviaciones
    dev_x = [xi - mean_x for xi in x]
    dev_y = [yi - mean_y for yi in y]
    
    # Suma de productos de desviaciones
    sum_dev_xy = sum(dx * dy for dx, dy in zip(dev_x, dev_y))
    
    # Suma de cuadrados de desviaciones
    sum_dev_x2 = sum(dx ** 2 for dx in dev_x)
    sum_dev_y2 = sum(dy ** 2 for dy in dev_y)
    
    # Evitar división por cero
    denominator = (sum_dev_x2 * sum_dev_y2) ** 0.5
    if denominator == 0:
        return 0
    
    return sum_dev_xy / denominator


def interpret_correlation(r):
    """Interpreta el coeficiente de correlación."""
    abs_r = abs(r)
    
    if abs_r >= 0.9:
        strength = "muy fuerte"
    elif abs_r >= 0.7:
        strength = "fuerte"
    elif abs_r >= 0.5:
        strength = "moderada"
    elif abs_r >= 0.3:
        strength = "débil"
    else:
        strength = "muy débil o inexistente"
    
    if r > 0:
        direction = "positiva"
        explanation = "Cuando una aumenta, la otra tiende a aumentar"
    elif r < 0:
        direction = "negativa"
        explanation = "Cuando una aumenta, la otra tiende a disminuir"
    else:
        direction = ""
        explanation = "No hay relación lineal aparente"
    
    return {
        'strength': strength,
        'direction': direction,
        'explanation': explanation
    }
