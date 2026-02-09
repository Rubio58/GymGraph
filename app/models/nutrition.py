"""
Modelos de Nutrición
"""

from app.models.database import Database


class Food:
    """Modelo para alimentos."""
    
    def __init__(self, id=None, user_id=None, created_by=None, name=None, brand=None,
                 serving_size=100, serving_unit='g', calories=0,
                 protein_g=0, carbs_g=0, fat_g=0, fiber_g=0, 
                 sugar_g=0, sodium_mg=0, is_custom=False, created_at=None):
        self.id = id
        self.user_id = user_id or created_by  # Acepta ambos nombres
        self.name = name
        self.brand = brand
        self.serving_size = serving_size
        self.serving_unit = serving_unit
        self.calories = calories
        self.protein_g = protein_g
        self.carbs_g = carbs_g
        self.fat_g = fat_g
        self.fiber_g = fiber_g
        self.sugar_g = sugar_g
        self.sodium_mg = sodium_mg
        self.is_custom = is_custom
        self.created_at = created_at
    
    def save(self):
        """Guarda el alimento."""
        if self.id is None:
            query = """
                INSERT INTO foods 
                (created_by, name, brand, serving_size, serving_unit, calories,
                 protein_g, carbs_g, fat_g, fiber_g, is_custom)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.user_id, self.name, self.brand, self.serving_size,
                     self.serving_unit, self.calories, self.protein_g, 
                     self.carbs_g, self.fat_g, self.fiber_g, self.is_custom)
            self.id = Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_all(cls, user_id=None):
        """Obtiene todos los alimentos."""
        query = """
            SELECT * FROM foods 
            WHERE is_custom = 0 OR created_by = %s
            ORDER BY name
        """
        results = Database.execute_query(query, (user_id,))
        return [cls(**row) for row in results]
    
    @classmethod
    def search(cls, search_term, user_id=None):
        """Busca alimentos por nombre."""
        query = """
            SELECT * FROM foods 
            WHERE (is_custom = 0 OR created_by = %s)
            AND (name LIKE %s OR brand LIKE %s)
            ORDER BY name
            LIMIT 20
        """
        search = f"%{search_term}%"
        results = Database.execute_query(query, (user_id, search, search))
        return [cls(**row) for row in results]
    
    @classmethod
    def get_by_id(cls, food_id):
        """Obtiene un alimento por ID."""
        query = "SELECT * FROM foods WHERE id = %s"
        result = Database.execute_query(query, (food_id,), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'serving_size': float(self.serving_size),
            'serving_unit': self.serving_unit,
            'calories': float(self.calories),
            'protein_g': float(self.protein_g),
            'carbs_g': float(self.carbs_g),
            'fat_g': float(self.fat_g),
            'fiber_g': float(self.fiber_g),
            'is_custom': self.is_custom
        }


class NutritionGoal:
    """Modelo para objetivos nutricionales."""
    
    def __init__(self, id=None, user_id=None, daily_calories=None,
                 protein_g=None, carbs_g=None, fat_g=None, 
                 water_liters=None, updated_at=None,
                 # Nombres alternativos de la tabla
                 calories_target=None, protein_target=None, 
                 carbs_target=None, fat_target=None, water_target_ml=None,
                 created_at=None):
        self.id = id
        self.user_id = user_id
        # Aceptar ambos nombres de columnas
        self.daily_calories = daily_calories or calories_target
        self.protein_g = protein_g or protein_target
        self.carbs_g = carbs_g or carbs_target
        self.fat_g = fat_g or fat_target
        self.water_liters = water_liters or (water_target_ml / 1000 if water_target_ml else None)
        self.updated_at = updated_at or created_at
    
    def save(self):
        """Guarda los objetivos nutricionales."""
        # Usar nombres de columnas que existen en la tabla
        water_ml = int(self.water_liters * 1000) if self.water_liters else 2000
        query = """
            INSERT INTO nutrition_goals 
            (user_id, calories_target, protein_target, carbs_target, fat_target, water_target_ml)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            calories_target = VALUES(calories_target),
            protein_target = VALUES(protein_target),
            carbs_target = VALUES(carbs_target),
            fat_target = VALUES(fat_target),
            water_target_ml = VALUES(water_target_ml)
        """
        params = (self.user_id, self.daily_calories, self.protein_g,
                 self.carbs_g, self.fat_g, water_ml)
        Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_user(cls, user_id):
        """Obtiene objetivos de un usuario."""
        query = "SELECT * FROM nutrition_goals WHERE user_id = %s"
        result = Database.execute_query(query, (user_id,), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'daily_calories': self.daily_calories,
            'protein_g': self.protein_g,
            'carbs_g': self.carbs_g,
            'fat_g': self.fat_g,
            'water_liters': float(self.water_liters) if self.water_liters else None
        }


class FoodLog:
    """Modelo para registro de alimentos."""
    
    def __init__(self, id=None, user_id=None, food_id=None, recipe_id=None,
                 log_date=None, meal_type=None, quantity=None, unit='g',
                 created_at=None, **kwargs):
        self.id = id
        self.user_id = user_id
        self.food_id = food_id
        self.recipe_id = recipe_id
        self.log_date = log_date
        self.meal_type = meal_type
        self.quantity = quantity
        self.unit = unit
        self.created_at = created_at
    
    def save(self):
        """Guarda el registro."""
        if self.id is None:
            # La tabla no tiene columna 'unit', omitirla
            query = """
                INSERT INTO food_logs 
                (user_id, food_id, log_date, meal_type, quantity)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (self.user_id, self.food_id, 
                     self.log_date, self.meal_type, self.quantity)
            self.id = Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_date(cls, user_id, log_date):
        """Obtiene registros de un día."""
        query = """
            SELECT fl.*, f.name as food_name, f.calories, f.protein_g, 
                   f.carbs_g, f.fat_g, f.serving_size
            FROM food_logs fl
            LEFT JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = %s AND fl.log_date = %s
            ORDER BY fl.meal_type, fl.created_at
        """
        return Database.execute_query(query, (user_id, log_date))
    
    @classmethod
    def get_daily_totals(cls, user_id, log_date):
        """Obtiene totales nutricionales del día."""
        query = """
            SELECT 
                SUM((f.calories / f.serving_size) * fl.quantity) as total_calories,
                SUM((f.protein_g / f.serving_size) * fl.quantity) as total_protein,
                SUM((f.carbs_g / f.serving_size) * fl.quantity) as total_carbs,
                SUM((f.fat_g / f.serving_size) * fl.quantity) as total_fat
            FROM food_logs fl
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = %s AND fl.log_date = %s
        """
        return Database.execute_query(query, (user_id, log_date), fetch_one=True)
    
    def delete(self):
        """Elimina el registro."""
        query = "DELETE FROM food_logs WHERE id = %s"
        return Database.execute_update(query, (self.id,))


class WaterLog:
    """Modelo para registro de agua."""
    
    def __init__(self, id=None, user_id=None, log_date=None, 
                 liters=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.log_date = log_date
        self.liters = liters
        self.created_at = created_at
    
    def save(self):
        """Guarda o actualiza el registro de agua."""
        query = """
            INSERT INTO water_logs (user_id, log_date, liters)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE liters = VALUES(liters)
        """
        params = (self.user_id, self.log_date, self.liters)
        Database.execute_insert(query, params)
        return self
    
    @classmethod
    def get_by_date(cls, user_id, log_date):
        """Obtiene registro de agua de un día."""
        query = "SELECT * FROM water_logs WHERE user_id = %s AND log_date = %s"
        result = Database.execute_query(query, (user_id, log_date), fetch_one=True)
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def add_water(cls, user_id, log_date, liters_to_add):
        """Añade agua al registro del día."""
        existing = cls.get_by_date(user_id, log_date)
        if existing:
            existing.liters = float(existing.liters) + liters_to_add
            return existing.save()
        else:
            new_log = cls(user_id=user_id, log_date=log_date, liters=liters_to_add)
            return new_log.save()
