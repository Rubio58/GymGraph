# controllers/measurement_controller.py
from datetime import datetime
from flask import  render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from services.measurement_service import MeasurementService

measurement_bp = Blueprint('measurement', __name__, url_prefix='/measurement')

@measurement_bp.route('/')
@login_required
def index():
    """Página principal de medidas corporales"""
    meas_service = MeasurementService()
    meascats = meas_service.get_meascats()
    
    return render_template(
        'measurement/index.html',
        meascats=meascats
    )

import json

@measurement_bp.route('/get-measurements-html/<int:meascat_id>')
@login_required
def get_measurements(meascat_id):
    meas_service = MeasurementService()
    measurements= meas_service.get_measurements_by_cat(meascat_id, current_user.id)
    unit = meas_service.get_meascat_unit(meascat_id)
    category_name = meas_service.get_meascat_name(meascat_id)
   
    # Data for the chart (must be chronological: oldest to newest)
    chart_labels = []
    chart_data = []
    for m in reversed(measurements):
        dt = m['date']
        label = dt.strftime('%Y-%m-%d') if hasattr(dt, 'strftime') else str(dt).split(' ')[0]
        chart_labels.append(label)
        chart_data.append(float(m['val']))

    # Renderizar el template parcial 
    return render_template(
        'measurement/measurements.html',
        measurements=measurements,
        meascat_id=meascat_id,
        unit=unit,
        category_name=category_name,
        chart_labels=json.dumps(chart_labels),
        chart_data=json.dumps(chart_data)
    )

@measurement_bp.route('/create-measurement', methods=['POST'])
@login_required
def create_measurement():
    try:
        val = float(request.form.get('val'))
        cat_id = int(request.form.get('meascat_id'))
    except (ValueError, TypeError):
        return "Invalid input", 400

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_id = current_user.id

    meas_service = MeasurementService()
    meas_service.create_measurement(val, current_date, cat_id, user_id)
    
    return get_measurements(cat_id)

@measurement_bp.route('/delete-measurement', methods=['POST'])
@login_required
def delete_measurement():
    try:
        meascat_id = int(request.form.get('meascat_id'))
        meas_id = int(request.form.get('meas_id'))
    except (ValueError, TypeError):
        return "Invalid input", 400
        
    meas_service = MeasurementService()
    meas_service.delete_measurement(meas_id)
    
    return get_measurements(meascat_id)