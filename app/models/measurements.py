"""
Modelos de Medidas Corporales y Autocuidado
"""

from app.models.database import Database


class BodyMeasurement:
    """Modelo para medidas corporales."""
    
    def __init__(self, id=None, user_id=None, measurement_date=None,
                 weight_kg=None, body_fat_percentage=None, chest_cm=None,
                 waist_cm=None, hips_cm=None, bicep_left_cm=None, 
                 bicep_right_cm=None, thigh_left_cm=None, thigh_right_cm=None,
                 calf_left_cm=None, calf_right_cm=None, neck_cm=None,
                 shoulders_cm=None, notes=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.measurement_date = measurement_date
        self.weight_kg = weight_kg
        self.body_fat_percentage = body_fat_percentage
        self.chest_cm = chest_cm
        self.waist_cm = waist_cm
        self.hips_cm = hips_cm
        self.bicep_left_cm = bicep_left_cm
        self.bicep_right_cm = bicep_right_cm
        self.thigh_left_cm = thigh_left_cm
        self.thigh_right_cm = thigh_right_cm
        self.calf_left_cm = calf_left_cm
        self.calf_right_cm = calf_right_cm
        self.neck_cm = neck_cm
        self.shoulders_cm = shoulders_cm
        self.notes = notes
        self.created_at = created_at
    
    def save(self):
        """Guarda las medidas."""
        if self.id is None:
            query = """
                INSERT INTO body_measurements 
                (user_id, measurement_date, weight_kg, body_fat_percentage,
                 chest_cm, waist_cm, hips_cm, bicep_left_cm, bicep_right_cm,
                 thigh_left_cm, thigh_right_cm, calf_left_cm, calf_right_cm,
                 neck_cm, shoulders_cm, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.user_id, self.measurement_date, self.weight_kg,
                     self.body_fat_percentage, self.chest_cm, self.waist_cm,
                     self.hips_cm, self.bicep_left_cm, self.bicep_right_cm,
                     self.thigh_left_cm, self.thigh_right_cm, self.calf_left_cm,
                     self.calf_right_cm, self.neck_cm, self.shoulders_cm, self.notes)
            self.id = Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_user(cls, user_id, limit=30):
        """Obtiene medidas de un usuario."""
        query = """
            SELECT * FROM body_measurements 
            WHERE user_id = %s 
            ORDER BY measurement_date DESC
            LIMIT %s
        """
        results = Database.execute_query(query, (user_id, limit))
        return [cls(**row) for row in results]
    
    @classmethod
    def get_latest(cls, user_id):
        """Obtiene las últimas medidas."""
        query = """
            SELECT * FROM body_measurements 
            WHERE user_id = %s 
            ORDER BY measurement_date DESC
            LIMIT 1
        """
        result = Database.execute_query(query, (user_id,), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def get_weight_history(cls, user_id, days=90):
        """Obtiene historial de peso."""
        query = """
            SELECT measurement_date, weight_kg
            FROM body_measurements 
            WHERE user_id = %s AND weight_kg IS NOT NULL
            AND measurement_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            ORDER BY measurement_date
        """
        return Database.execute_query(query, (user_id, days))
    
    def to_dict(self):
        return {
            'id': self.id,
            'measurement_date': str(self.measurement_date) if self.measurement_date else None,
            'weight_kg': float(self.weight_kg) if self.weight_kg else None,
            'body_fat_percentage': float(self.body_fat_percentage) if self.body_fat_percentage else None,
            'chest_cm': float(self.chest_cm) if self.chest_cm else None,
            'waist_cm': float(self.waist_cm) if self.waist_cm else None,
            'hips_cm': float(self.hips_cm) if self.hips_cm else None,
            'bicep_left_cm': float(self.bicep_left_cm) if self.bicep_left_cm else None,
            'bicep_right_cm': float(self.bicep_right_cm) if self.bicep_right_cm else None,
            'thigh_left_cm': float(self.thigh_left_cm) if self.thigh_left_cm else None,
            'thigh_right_cm': float(self.thigh_right_cm) if self.thigh_right_cm else None,
            'notes': self.notes
        }


class SleepLog:
    """Modelo para registro de sueño."""
    
    def __init__(self, id=None, user_id=None, log_date=None,
                 hours_slept=None, sleep_quality=None, notes=None, 
                 created_at=None):
        self.id = id
        self.user_id = user_id
        self.log_date = log_date
        self.hours_slept = hours_slept
        self.sleep_quality = sleep_quality
        self.notes = notes
        self.created_at = created_at
    
    def save(self):
        """Guarda el registro de sueño."""
        query = """
            INSERT INTO sleep_logs (user_id, log_date, hours_slept, sleep_quality, notes)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            hours_slept = VALUES(hours_slept),
            sleep_quality = VALUES(sleep_quality),
            notes = VALUES(notes)
        """
        params = (self.user_id, self.log_date, self.hours_slept, 
                 self.sleep_quality, self.notes)
        Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_user(cls, user_id, days=30):
        """Obtiene registros de sueño."""
        query = """
            SELECT * FROM sleep_logs 
            WHERE user_id = %s 
            AND log_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            ORDER BY log_date DESC
        """
        results = Database.execute_query(query, (user_id, days))
        return [cls(**row) for row in results]
    
    def to_dict(self):
        return {
            'log_date': str(self.log_date) if self.log_date else None,
            'hours_slept': float(self.hours_slept) if self.hours_slept else None,
            'sleep_quality': self.sleep_quality,
            'notes': self.notes
        }


class MenstrualLog:
    """Modelo para registro de ciclo menstrual."""
    
    def __init__(self, id=None, user_id=None, log_date=None,
                 is_period_day=True, flow_intensity=None, symptoms=None,
                 notes=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.log_date = log_date
        self.is_period_day = is_period_day
        self.flow_intensity = flow_intensity
        self.symptoms = symptoms
        self.notes = notes
        self.created_at = created_at
    
    def save(self):
        """Guarda el registro."""
        query = """
            INSERT INTO menstrual_logs 
            (user_id, log_date, is_period_day, flow_intensity, symptoms, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            is_period_day = VALUES(is_period_day),
            flow_intensity = VALUES(flow_intensity),
            symptoms = VALUES(symptoms),
            notes = VALUES(notes)
        """
        params = (self.user_id, self.log_date, self.is_period_day,
                 self.flow_intensity, self.symptoms, self.notes)
        Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_user(cls, user_id, months=3):
        """Obtiene registros menstruales."""
        query = """
            SELECT * FROM menstrual_logs 
            WHERE user_id = %s 
            AND log_date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
            ORDER BY log_date DESC
        """
        results = Database.execute_query(query, (user_id, months))
        return [cls(**row) for row in results]


class StepLog:
    """Modelo para registro de pasos."""
    
    def __init__(self, id=None, user_id=None, log_date=None,
                 steps=0, created_at=None):
        self.id = id
        self.user_id = user_id
        self.log_date = log_date
        self.steps = steps
        self.created_at = created_at
    
    def save(self):
        """Guarda el registro de pasos."""
        query = """
            INSERT INTO step_logs (user_id, log_date, steps)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE steps = VALUES(steps)
        """
        params = (self.user_id, self.log_date, self.steps)
        Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_user(cls, user_id, days=30):
        """Obtiene registros de pasos."""
        query = """
            SELECT * FROM step_logs 
            WHERE user_id = %s 
            AND log_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            ORDER BY log_date DESC
        """
        results = Database.execute_query(query, (user_id, days))
        return [cls(**row) for row in results]
