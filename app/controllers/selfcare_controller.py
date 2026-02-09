"""
Controlador de Autocuidado
"""

from flask import Blueprint, request, render_template, session, jsonify, flash, redirect, url_for
from datetime import date
# Sin autenticación - aplicación local
from app.models.measurements import SleepLog, MenstrualLog, StepLog

selfcare_bp = Blueprint('selfcare', __name__)


# ============================================
# VISTAS HTML
# ============================================

@selfcare_bp.route('/')

def index():
    """Vista principal de autocuidado."""
    user_id = session['user_id']
    
    sleep_logs = SleepLog.get_by_user(user_id, days=7)
    step_logs = StepLog.get_by_user(user_id, days=7)
    menstrual_logs = MenstrualLog.get_by_user(user_id, months=1)
    
    return render_template('selfcare/index.html',
                         sleep_logs=sleep_logs,
                         step_logs=step_logs,
                         menstrual_logs=menstrual_logs,
                         today=date.today())


@selfcare_bp.route('/sleep', methods=['GET', 'POST'])

def sleep():
    """Registro de sueño."""
    user_id = session['user_id']
    
    if request.method == 'POST':
        log = SleepLog(
            user_id=user_id,
            log_date=request.form.get('log_date') or date.today(),
            hours_slept=float(request.form.get('hours_slept', 0)),
            sleep_quality=int(request.form.get('sleep_quality', 5)),
            notes=request.form.get('notes')
        )
        log.save()
        
        flash('Sueño registrado', 'success')
        return redirect(url_for('selfcare.index'))
    
    sleep_logs = SleepLog.get_by_user(user_id, days=30)
    return render_template('selfcare/sleep.html', logs=sleep_logs)


@selfcare_bp.route('/steps', methods=['GET', 'POST'])

def steps():
    """Registro de pasos."""
    user_id = session['user_id']
    
    if request.method == 'POST':
        log = StepLog(
            user_id=user_id,
            log_date=request.form.get('log_date') or date.today(),
            steps=int(request.form.get('steps', 0))
        )
        log.save()
        
        flash('Pasos registrados', 'success')
        return redirect(url_for('selfcare.index'))
    
    step_logs = StepLog.get_by_user(user_id, days=30)
    return render_template('selfcare/steps.html', logs=step_logs)


@selfcare_bp.route('/menstrual', methods=['GET', 'POST'])

def menstrual():
    """Registro menstrual."""
    user_id = session['user_id']
    
    if request.method == 'POST':
        # Nueva lógica: flow_option puede ser 'none', 'light', 'medium', 'heavy'
        flow_option = request.form.get('flow_option', 'none')
        
        if flow_option == 'none':
            is_period_day = False
            flow_intensity = None
        else:
            is_period_day = True
            flow_intensity = flow_option
        
        log = MenstrualLog(
            user_id=user_id,
            log_date=request.form.get('log_date') or date.today(),
            is_period_day=is_period_day,
            flow_intensity=flow_intensity,
            symptoms=request.form.get('symptoms'),
            notes=request.form.get('notes')
        )
        log.save()
        
        flash('Registro guardado', 'success')
        return redirect(url_for('selfcare.index'))
    
    logs = MenstrualLog.get_by_user(user_id, months=3)
    return render_template('selfcare/menstrual.html', logs=logs)


# ============================================
# API ENDPOINTS
# ============================================

@selfcare_bp.route('/api/sleep', methods=['POST'])

def api_add_sleep():
    """API: Registrar sueño."""
    data = request.json
    user_id = session['user_id']
    
    log = SleepLog(
        user_id=user_id,
        log_date=data.get('log_date', date.today().isoformat()),
        hours_slept=data.get('hours_slept'),
        sleep_quality=data.get('sleep_quality'),
        notes=data.get('notes')
    )
    log.save()
    
    return jsonify(log.to_dict()), 201


@selfcare_bp.route('/api/sleep')

def api_get_sleep():
    """API: Obtener historial de sueño."""
    user_id = session['user_id']
    days = request.args.get('days', 30, type=int)
    
    logs = SleepLog.get_by_user(user_id, days)
    return jsonify([log.to_dict() for log in logs])


@selfcare_bp.route('/api/steps', methods=['POST'])

def api_add_steps():
    """API: Registrar pasos."""
    data = request.json
    user_id = session['user_id']
    
    log = StepLog(
        user_id=user_id,
        log_date=data.get('log_date', date.today().isoformat()),
        steps=data.get('steps', 0)
    )
    log.save()
    
    return jsonify({'message': 'Pasos registrados'}), 201


@selfcare_bp.route('/api/steps')

def api_get_steps():
    """API: Obtener historial de pasos."""
    user_id = session['user_id']
    days = request.args.get('days', 30, type=int)
    
    logs = StepLog.get_by_user(user_id, days)
    return jsonify([{
        'log_date': str(log.log_date),
        'steps': log.steps
    } for log in logs])


@selfcare_bp.route('/api/menstrual', methods=['POST'])

def api_add_menstrual():
    """API: Registrar menstruación."""
    data = request.json
    user_id = session['user_id']
    
    log = MenstrualLog(
        user_id=user_id,
        log_date=data.get('log_date', date.today().isoformat()),
        is_period_day=data.get('is_period_day', True),
        flow_intensity=data.get('flow_intensity'),
        symptoms=data.get('symptoms'),
        notes=data.get('notes')
    )
    log.save()
    
    return jsonify({'message': 'Registro guardado'}), 201
