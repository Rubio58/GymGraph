"""
Modelos de Entrenamiento
"""

from app.models.database import Database


class Exercise:
    """Modelo para ejercicios."""
    
    def __init__(self, id=None, name=None, description=None, muscle_group=None,
                 equipment=None, created_by=None, is_custom=False, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.muscle_group = muscle_group
        self.equipment = equipment
        self.created_by = created_by
        self.is_custom = is_custom
        self.created_at = created_at
    
    def save(self):
        """Guarda el ejercicio."""
        if self.id is None:
            query = """
                INSERT INTO exercises (name, description, muscle_group, equipment, 
                                       created_by, is_custom)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (self.name, self.description, self.muscle_group, 
                     self.equipment, self.created_by, self.is_custom)
            self.id = Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_all(cls, user_id=None):
        """Obtiene todos los ejercicios disponibles para un usuario."""
        query = """
            SELECT * FROM exercises 
            WHERE is_custom = FALSE OR created_by = %s
            ORDER BY muscle_group, name
        """
        results = Database.execute_query(query, (user_id,))
        return [cls(**row) for row in results]
    
    @classmethod
    def get_by_id(cls, exercise_id):
        """Obtiene un ejercicio por ID."""
        query = "SELECT * FROM exercises WHERE id = %s"
        result = Database.execute_query(query, (exercise_id,), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def get_by_muscle_group(cls, muscle_group, user_id=None):
        """Obtiene ejercicios por grupo muscular."""
        query = """
            SELECT * FROM exercises 
            WHERE muscle_group = %s AND (is_custom = FALSE OR created_by = %s)
            ORDER BY name
        """
        results = Database.execute_query(query, (muscle_group, user_id))
        return [cls(**row) for row in results]
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'muscle_group': self.muscle_group,
            'equipment': self.equipment,
            'is_custom': self.is_custom
        }


class TrainingPlan:
    """Modelo para planes de entrenamiento."""
    
    def __init__(self, id=None, user_id=None, name=None, description=None,
                 is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    def save(self):
        """Guarda el plan de entrenamiento."""
        if self.id is None:
            query = """
                INSERT INTO training_plans (user_id, name, description, is_active)
                VALUES (%s, %s, %s, %s)
            """
            params = (self.user_id, self.name, self.description, self.is_active)
            self.id = Database.execute_insert(query, params)
        else:
            query = """
                UPDATE training_plans 
                SET name=%s, description=%s, is_active=%s
                WHERE id=%s
            """
            params = (self.name, self.description, self.is_active, self.id)
            Database.execute_update(query, params)
        return self
    
    @classmethod
    def get_by_user(cls, user_id):
        """Obtiene planes de un usuario."""
        query = "SELECT * FROM training_plans WHERE user_id = %s ORDER BY created_at DESC"
        results = Database.execute_query(query, (user_id,))
        return [cls(**row) for row in results]
    
    @classmethod
    def get_active_plan(cls, user_id):
        """Obtiene el plan activo del usuario."""
        query = "SELECT * FROM training_plans WHERE user_id = %s AND is_active = TRUE LIMIT 1"
        result = Database.execute_query(query, (user_id,), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    def get_days(self):
        """Obtiene los días del plan."""
        return TrainingDay.get_by_plan(self.id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'days': [day.to_dict() for day in self.get_days()]
        }


class TrainingDay:
    """Modelo para días de entrenamiento."""
    
    def __init__(self, id=None, plan_id=None, day_of_week=None, name=None):
        self.id = id
        self.plan_id = plan_id
        self.day_of_week = day_of_week
        self.name = name
    
    def save(self):
        """Guarda el día de entrenamiento."""
        if self.id is None:
            query = """
                INSERT INTO training_days (plan_id, day_of_week, name)
                VALUES (%s, %s, %s)
            """
            params = (self.plan_id, self.day_of_week, self.name)
            self.id = Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_plan(cls, plan_id):
        """Obtiene días de un plan."""
        query = "SELECT * FROM training_days WHERE plan_id = %s ORDER BY day_of_week"
        results = Database.execute_query(query, (plan_id,))
        return [cls(**row) for row in results]
    
    def get_exercises(self):
        """Obtiene los ejercicios planificados del día."""
        return PlannedExercise.get_by_day(self.id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'plan_id': self.plan_id,
            'day_of_week': self.day_of_week,
            'name': self.name,
            'exercises': [ex.to_dict() for ex in self.get_exercises()]
        }


class PlannedExercise:
    """Modelo para ejercicios planificados."""
    
    def __init__(self, id=None, training_day_id=None, exercise_id=None,
                 order_index=0, target_sets=None, target_reps=None, notes=None):
        self.id = id
        self.training_day_id = training_day_id
        self.exercise_id = exercise_id
        self.order_index = order_index
        self.target_sets = target_sets
        self.target_reps = target_reps
        self.notes = notes
    
    def save(self):
        """Guarda el ejercicio planificado."""
        if self.id is None:
            query = """
                INSERT INTO planned_exercises 
                (training_day_id, exercise_id, order_index, target_sets, target_reps, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (self.training_day_id, self.exercise_id, self.order_index,
                     self.target_sets, self.target_reps, self.notes)
            self.id = Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_day(cls, training_day_id):
        """Obtiene ejercicios de un día."""
        query = """
            SELECT pe.*, e.name as exercise_name, e.muscle_group
            FROM planned_exercises pe
            JOIN exercises e ON pe.exercise_id = e.id
            WHERE pe.training_day_id = %s
            ORDER BY pe.order_index
        """
        results = Database.execute_query(query, (training_day_id,))
        return results
    
    def to_dict(self):
        return {
            'id': self.id,
            'training_day_id': self.training_day_id,
            'exercise_id': self.exercise_id,
            'order_index': self.order_index,
            'target_sets': self.target_sets,
            'target_reps': self.target_reps,
            'notes': self.notes
        }


class WorkoutSession:
    """Modelo para sesiones de entrenamiento."""
    
    def __init__(self, id=None, user_id=None, training_day_id=None, 
                 session_date=None, start_time=None, end_time=None, 
                 notes=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.training_day_id = training_day_id
        self.session_date = session_date
        self.start_time = start_time
        self.end_time = end_time
        self.notes = notes
        self.created_at = created_at
    
    def save(self):
        """Guarda la sesión."""
        if self.id is None:
            query = """
                INSERT INTO workout_sessions 
                (user_id, training_day_id, session_date, start_time, end_time, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            # Convertir time objects a strings para SQLite
            start_str = str(self.start_time) if self.start_time else None
            end_str = str(self.end_time) if self.end_time else None
            params = (self.user_id, self.training_day_id, self.session_date,
                     start_str, end_str, self.notes)
            self.id = Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_user(cls, user_id, limit=10):
        """Obtiene sesiones de un usuario."""
        query = """
            SELECT * FROM workout_sessions 
            WHERE user_id = %s 
            ORDER BY session_date DESC, start_time DESC
            LIMIT %s
        """
        results = Database.execute_query(query, (user_id, limit))
        return [cls(**row) for row in results]
    
    @classmethod
    def get_latest(cls, user_id):
        """Obtiene la última sesión de un usuario."""
        query = """
            SELECT * FROM workout_sessions 
            WHERE user_id = %s 
            ORDER BY session_date DESC, start_time DESC
            LIMIT 1
        """
        result = Database.execute_query(query, (user_id,), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    def get_sets(self):
        """Obtiene las series de la sesión."""
        return WorkoutSet.get_by_session(self.id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'training_day_id': self.training_day_id,
            'session_date': str(self.session_date) if self.session_date else None,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'notes': self.notes
        }


class WorkoutSet:
    """Modelo para series de entrenamiento."""
    
    def __init__(self, id=None, session_id=None, exercise_id=None, set_number=None,
                 weight_kg=None, reps=None, rpe=None, is_warmup=False, 
                 notes=None, created_at=None):
        self.id = id
        self.session_id = session_id
        self.exercise_id = exercise_id
        self.set_number = set_number
        self.weight_kg = weight_kg
        self.reps = reps
        self.rpe = rpe
        self.is_warmup = is_warmup
        self.notes = notes
        self.created_at = created_at
    
    def save(self):
        """Guarda la serie."""
        if self.id is None:
            query = """
                INSERT INTO workout_sets 
                (session_id, exercise_id, set_number, weight_kg, reps, rpe, is_warmup, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.session_id, self.exercise_id, self.set_number,
                     self.weight_kg, self.reps, self.rpe, self.is_warmup, self.notes)
            self.id = Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_session(cls, session_id):
        """Obtiene series de una sesión."""
        query = """
            SELECT ws.*, e.name as exercise_name
            FROM workout_sets ws
            JOIN exercises e ON ws.exercise_id = e.id
            WHERE ws.session_id = %s
            ORDER BY ws.exercise_id, ws.set_number
        """
        return Database.execute_query(query, (session_id,))
    
    @classmethod
    def get_exercise_history(cls, user_id, exercise_id, limit=20):
        """Obtiene historial de un ejercicio."""
        query = """
            SELECT ws.*, wss.session_date
            FROM workout_sets ws
            JOIN workout_sessions wss ON ws.session_id = wss.id
            WHERE wss.user_id = %s AND ws.exercise_id = %s
            ORDER BY wss.session_date DESC, ws.set_number
            LIMIT %s
        """
        return Database.execute_query(query, (user_id, exercise_id, limit))
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'exercise_id': self.exercise_id,
            'set_number': self.set_number,
            'weight_kg': float(self.weight_kg) if self.weight_kg else None,
            'reps': self.reps,
            'rpe': self.rpe,
            'is_warmup': self.is_warmup,
            'notes': self.notes
        }
