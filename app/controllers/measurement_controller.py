"""
Controlador de Medidas Corporales
"""

from flask import Blueprint, request, render_template, session, jsonify
from datetime import date
# Sin autenticación - aplicación local
from app.models.measurements import BodyMeasurement

measurement_bp = Blueprint('measurement', __name__)


# ============================================
# VISTAS HTML
# ============================================

@measurement_bp.route('/')

def index():
    """Vista principal de medidas."""
    user_id = session['user_id']
    measurements = BodyMeasurement.get_by_user(user_id, limit=10)
    latest = BodyMeasurement.get_latest(user_id)
    
    return render_template('measurement/index.html',
                         measurements=measurements,
                         latest=latest)


@measurement_bp.route('/new', methods=['GET', 'POST'])

def new_measurement():
    """Registrar nuevas medidas."""
    if request.method == 'POST':
        user_id = session['user_id']
        
        measurement = BodyMeasurement(
            user_id=user_id,
            measurement_date=request.form.get('measurement_date') or date.today(),
            weight_kg=request.form.get('weight_kg') or None,
            body_fat_percentage=request.form.get('body_fat_percentage') or None,
            chest_cm=request.form.get('chest_cm') or None,
            waist_cm=request.form.get('waist_cm') or None,
            hips_cm=request.form.get('hips_cm') or None,
            bicep_left_cm=request.form.get('bicep_left_cm') or None,
            bicep_right_cm=request.form.get('bicep_right_cm') or None,
            thigh_left_cm=request.form.get('thigh_left_cm') or None,
            thigh_right_cm=request.form.get('thigh_right_cm') or None,
            calf_left_cm=request.form.get('calf_left_cm') or None,
            calf_right_cm=request.form.get('calf_right_cm') or None,
            neck_cm=request.form.get('neck_cm') or None,
            shoulders_cm=request.form.get('shoulders_cm') or None,
            notes=request.form.get('notes')
        )
        measurement.save()
        
        from flask import flash, redirect, url_for
        flash('Medidas registradas correctamente', 'success')
        return redirect(url_for('measurement.index'))
    
    return render_template('measurement/new.html', today=date.today())


# ============================================
# API ENDPOINTS
# ============================================

@measurement_bp.route('/api/measurements')

def api_measurements():
    """API: Obtener historial de medidas."""
    user_id = session['user_id']
    limit = request.args.get('limit', 30, type=int)
    
    measurements = BodyMeasurement.get_by_user(user_id, limit)
    return jsonify([m.to_dict() for m in measurements])


@measurement_bp.route('/api/measurements', methods=['POST'])

def api_add_measurement():
    """API: Añadir medida."""
    data = request.json
    user_id = session['user_id']
    
    measurement = BodyMeasurement(
        user_id=user_id,
        measurement_date=data.get('measurement_date', date.today().isoformat()),
        weight_kg=data.get('weight_kg'),
        body_fat_percentage=data.get('body_fat_percentage'),
        chest_cm=data.get('chest_cm'),
        waist_cm=data.get('waist_cm'),
        hips_cm=data.get('hips_cm'),
        bicep_left_cm=data.get('bicep_left_cm'),
        bicep_right_cm=data.get('bicep_right_cm'),
        thigh_left_cm=data.get('thigh_left_cm'),
        thigh_right_cm=data.get('thigh_right_cm'),
        calf_left_cm=data.get('calf_left_cm'),
        calf_right_cm=data.get('calf_right_cm'),
        neck_cm=data.get('neck_cm'),
        shoulders_cm=data.get('shoulders_cm'),
        notes=data.get('notes')
    )
    measurement.save()
    
    return jsonify(measurement.to_dict()), 201


@measurement_bp.route('/api/weight-history')

def api_weight_history():
    """API: Historial de peso para gráficas."""
    user_id = session['user_id']
    days = request.args.get('days', 90, type=int)
    
    history = BodyMeasurement.get_weight_history(user_id, days)
    return jsonify(history)


@measurement_bp.route('/api/latest')

def api_latest():
    """API: Últimas medidas."""
    user_id = session['user_id']
    latest = BodyMeasurement.get_latest(user_id)
    
    if latest:
        return jsonify(latest.to_dict())
    return jsonify({})
