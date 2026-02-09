#!/usr/bin/env python3
"""
Script para rellenar la base de datos con datos semi-realistas
"""

import sqlite3
import random
from datetime import date, timedelta

DB_PATH = 'data/gymgraph.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def clear_all_data(conn):
    """Borra todos los datos de la base de datos."""
    cursor = conn.cursor()
    tables = [
        'workout_sets', 'workout_sessions', 'planned_exercises', 
        'training_days', 'training_plans', 'food_logs', 'water_logs',
        'menstrual_logs', 'step_logs', 'sleep_logs', 'body_measurements',
        'nutrition_goals', 'foods', 'exercises'
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
    conn.commit()
    print("🗑️  Todos los datos borrados")

def seed_foods(conn):
    """Inserta alimentos comunes."""
    foods = [
        # Proteínas
        ('Pechuga de pollo', None, 100, 'g', 165, 31, 0, 3.6, 0),
        ('Huevo entero', None, 50, 'g', 78, 6, 0.6, 5, 0),
        ('Clara de huevo', None, 33, 'g', 17, 3.6, 0.2, 0, 0),
        ('Salmón', None, 100, 'g', 208, 20, 0, 13, 0),
        ('Atún en lata', 'Calvo', 100, 'g', 116, 26, 0, 1, 0),
        ('Ternera magra', None, 100, 'g', 250, 26, 0, 15, 0),
        ('Pavo', None, 100, 'g', 135, 30, 0, 1, 0),
        ('Merluza', None, 100, 'g', 89, 17, 0, 2, 0),
        ('Gambas', None, 100, 'g', 99, 24, 0.2, 0.3, 0),
        ('Tofu', None, 100, 'g', 76, 8, 1.9, 4.8, 0),
        
        # Carbohidratos
        ('Arroz blanco', None, 100, 'g', 130, 2.7, 28, 0.3, 0.4),
        ('Arroz integral', None, 100, 'g', 111, 2.6, 23, 0.9, 1.8),
        ('Pasta', None, 100, 'g', 131, 5, 25, 1.1, 1.8),
        ('Pan integral', 'Bimbo', 30, 'g', 69, 3.5, 12, 1, 2),
        ('Avena', 'Quaker', 40, 'g', 156, 5.3, 27, 2.8, 4),
        ('Patata', None, 100, 'g', 77, 2, 17, 0.1, 2.2),
        ('Boniato', None, 100, 'g', 86, 1.6, 20, 0.1, 3),
        ('Quinoa', None, 100, 'g', 120, 4.4, 21, 1.9, 2.8),
        ('Tortitas de arroz', None, 10, 'g', 39, 0.8, 8, 0.3, 0.3),
        
        # Verduras
        ('Brócoli', None, 100, 'g', 34, 2.8, 7, 0.4, 2.6),
        ('Espinacas', None, 100, 'g', 23, 2.9, 3.6, 0.4, 2.2),
        ('Tomate', None, 100, 'g', 18, 0.9, 3.9, 0.2, 1.2),
        ('Zanahoria', None, 100, 'g', 41, 0.9, 10, 0.2, 2.8),
        ('Calabacín', None, 100, 'g', 17, 1.2, 3.1, 0.3, 1),
        ('Pimiento rojo', None, 100, 'g', 31, 1, 6, 0.3, 2.1),
        ('Lechuga', None, 100, 'g', 15, 1.4, 2.9, 0.2, 1.3),
        ('Pepino', None, 100, 'g', 16, 0.7, 3.6, 0.1, 0.5),
        ('Cebolla', None, 100, 'g', 40, 1.1, 9, 0.1, 1.7),
        ('Champiñones', None, 100, 'g', 22, 3.1, 3.3, 0.3, 1),
        
        # Frutas
        ('Plátano', None, 120, 'g', 105, 1.3, 27, 0.4, 3.1),
        ('Manzana', None, 180, 'g', 95, 0.5, 25, 0.3, 4.4),
        ('Naranja', None, 130, 'g', 62, 1.2, 15, 0.2, 3.1),
        ('Fresas', None, 100, 'g', 32, 0.7, 7.7, 0.3, 2),
        ('Arándanos', None, 100, 'g', 57, 0.7, 14, 0.3, 2.4),
        ('Kiwi', None, 75, 'g', 42, 0.8, 10, 0.4, 2.1),
        ('Uvas', None, 100, 'g', 69, 0.7, 18, 0.2, 0.9),
        ('Sandía', None, 150, 'g', 45, 0.9, 11, 0.2, 0.6),
        ('Melón', None, 150, 'g', 54, 1.3, 13, 0.3, 1.4),
        
        # Lácteos
        ('Leche desnatada', 'Hacendado', 250, 'ml', 83, 8.3, 12, 0.3, 0),
        ('Yogur griego', 'Fage', 170, 'g', 100, 17, 6, 0.7, 0),
        ('Queso fresco batido', 'Hacendado', 100, 'g', 70, 10, 4, 0.2, 0),
        ('Requesón', None, 100, 'g', 98, 11, 3.4, 4.3, 0),
        ('Queso cottage', None, 100, 'g', 98, 11, 3.4, 4.3, 0),
        
        # Grasas saludables
        ('Aceite de oliva', None, 15, 'ml', 119, 0, 0, 13.5, 0),
        ('Aguacate', None, 100, 'g', 160, 2, 9, 15, 7),
        ('Almendras', None, 30, 'g', 173, 6, 6, 15, 4),
        ('Nueces', None, 30, 'g', 196, 4.6, 4, 20, 2),
        ('Mantequilla de cacahuete', None, 32, 'g', 188, 8, 6, 16, 2),
        ('Semillas de chía', None, 15, 'g', 73, 2.5, 6, 4.6, 5),
        
        # Suplementos
        ('Proteína whey', 'Optimum Nutrition', 30, 'g', 120, 24, 3, 1.5, 0),
        ('Creatina monohidrato', 'MyProtein', 5, 'g', 0, 0, 0, 0, 0),
        ('Barrita proteica', 'Quest', 60, 'g', 200, 21, 21, 8, 14),
        
        # Comidas preparadas
        ('Pizza margarita', None, 300, 'g', 750, 27, 90, 30, 3),
        ('Hamburguesa completa', None, 250, 'g', 550, 25, 40, 30, 2),
        ('Ensalada César', None, 250, 'g', 350, 20, 15, 25, 3),
        ('Wrap de pollo', None, 200, 'g', 350, 25, 30, 12, 2),
        ('Bowl de poke', None, 350, 'g', 450, 30, 50, 12, 3),
    ]
    
    cursor = conn.cursor()
    for food in foods:
        cursor.execute("""
            INSERT OR IGNORE INTO foods 
            (name, brand, serving_size, serving_unit, calories, protein_g, carbs_g, fat_g, fiber_g, created_by, is_custom)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0)
        """, food)
    conn.commit()
    print(f"✓ Insertados {len(foods)} alimentos")

def seed_exercises(conn):
    """Inserta ejercicios comunes."""
    exercises = [
        # Pecho
        ('Press banca', 'Acostado en banco, bajar barra al pecho y subir', 'chest', 'barbell'),
        ('Press inclinado mancuernas', 'Press en banco inclinado con mancuernas', 'chest', 'dumbbell'),
        ('Aperturas mancuernas', 'Acostado, brazos abiertos, juntar mancuernas arriba', 'chest', 'dumbbell'),
        ('Fondos en paralelas', 'Bajar cuerpo entre paralelas', 'chest', 'bodyweight'),
        ('Flexiones', 'Push-ups tradicionales', 'chest', 'bodyweight'),
        ('Press máquina pecho', 'Press en máquina de pecho', 'chest', 'machine'),
        ('Cruces en polea', 'Cruzar poleas delante del pecho', 'chest', 'cable'),
        
        # Espalda
        ('Dominadas', 'Pull-ups con agarre prono', 'back', 'bodyweight'),
        ('Jalón al pecho', 'Polea alta, tirar hacia el pecho', 'back', 'cable'),
        ('Remo con barra', 'Inclinado, tirar barra hacia abdomen', 'back', 'barbell'),
        ('Remo mancuerna', 'Apoyado en banco, tirar mancuerna', 'back', 'dumbbell'),
        ('Peso muerto', 'Levantar barra del suelo', 'back', 'barbell'),
        ('Remo en máquina', 'Remo sentado en máquina', 'back', 'machine'),
        ('Face pull', 'Tirar cuerda hacia la cara', 'back', 'cable'),
        
        # Hombros
        ('Press militar', 'Press con barra sobre la cabeza', 'shoulders', 'barbell'),
        ('Press Arnold', 'Press con rotación de mancuernas', 'shoulders', 'dumbbell'),
        ('Elevaciones laterales', 'Subir mancuernas a los lados', 'shoulders', 'dumbbell'),
        ('Elevaciones frontales', 'Subir mancuernas al frente', 'shoulders', 'dumbbell'),
        ('Pájaros', 'Elevaciones posteriores inclinado', 'shoulders', 'dumbbell'),
        ('Press hombro máquina', 'Press en máquina de hombros', 'shoulders', 'machine'),
        
        # Bíceps
        ('Curl con barra', 'Curl de bíceps con barra recta', 'biceps', 'barbell'),
        ('Curl mancuernas alterno', 'Curl alternando mancuernas', 'biceps', 'dumbbell'),
        ('Curl martillo', 'Curl con agarre neutro', 'biceps', 'dumbbell'),
        ('Curl concentrado', 'Curl apoyando codo en muslo', 'biceps', 'dumbbell'),
        ('Curl en polea', 'Curl usando polea baja', 'biceps', 'cable'),
        ('Curl predicador', 'Curl en banco predicador', 'biceps', 'barbell'),
        
        # Tríceps
        ('Press francés', 'Extensión de tríceps acostado', 'triceps', 'barbell'),
        ('Extensiones en polea', 'Empujar cuerda hacia abajo', 'triceps', 'cable'),
        ('Fondos en banco', 'Dips en banco', 'triceps', 'bodyweight'),
        ('Extensión mancuerna sobre cabeza', 'Extensión de tríceps overhead', 'triceps', 'dumbbell'),
        ('Patada de tríceps', 'Kickback con mancuerna', 'triceps', 'dumbbell'),
        
        # Piernas
        ('Sentadilla', 'Squat con barra', 'legs', 'barbell'),
        ('Prensa', 'Leg press en máquina', 'legs', 'machine'),
        ('Peso muerto rumano', 'Romanian deadlift', 'legs', 'barbell'),
        ('Zancadas', 'Lunges con mancuernas', 'legs', 'dumbbell'),
        ('Extensión de cuádriceps', 'Leg extension en máquina', 'legs', 'machine'),
        ('Curl femoral', 'Leg curl en máquina', 'legs', 'machine'),
        ('Hip thrust', 'Empuje de cadera', 'legs', 'barbell'),
        ('Elevación de gemelos', 'Calf raise', 'legs', 'machine'),
        ('Sentadilla búlgara', 'Bulgarian split squat', 'legs', 'dumbbell'),
        ('Peso muerto sumo', 'Sumo deadlift', 'legs', 'barbell'),
        
        # Core
        ('Plancha', 'Plank isométrico', 'core', 'bodyweight'),
        ('Crunch', 'Abdominales tradicionales', 'core', 'bodyweight'),
        ('Elevación de piernas', 'Leg raises colgado', 'core', 'bodyweight'),
        ('Russian twist', 'Giros con peso', 'core', 'dumbbell'),
        ('Ab wheel', 'Rueda abdominal', 'core', 'bodyweight'),
        ('Cable crunch', 'Crunch en polea', 'core', 'cable'),
        
        # Cardio
        ('Cinta de correr', 'Running en cinta', 'cardio', 'machine'),
        ('Bicicleta estática', 'Cycling indoor', 'cardio', 'machine'),
        ('Elíptica', 'Máquina elíptica', 'cardio', 'machine'),
        ('Remo ergómetro', 'Rowing machine', 'cardio', 'machine'),
        ('Saltar comba', 'Jump rope', 'cardio', 'bodyweight'),
    ]
    
    cursor = conn.cursor()
    for ex in exercises:
        cursor.execute("""
            INSERT OR IGNORE INTO exercises 
            (name, description, muscle_group, equipment, created_by, is_custom)
            VALUES (?, ?, ?, ?, NULL, 0)
        """, ex)
    conn.commit()
    print(f"✓ Insertados {len(exercises)} ejercicios")

def seed_measurements(conn):
    """Inserta medidas corporales de todo el año."""
    cursor = conn.cursor()
    today = date.today()
    
    # Simular progreso anual: empezar con más peso y grasa, ir bajando
    start_weight = 88.0
    start_fat = 25.0
    
    measurements = []
    for i in range(365, -1, -7):  # Cada 7 días durante 1 año
        d = today - timedelta(days=i)
        # Progreso gradual con algunas fluctuaciones
        progress = (365 - i) / 365
        # Simular mesetas y cambios estacionales
        seasonal_var = 1.5 * (1 + 0.3 * (1 if d.month in [12, 1, 2] else -0.5 if d.month in [6, 7, 8] else 0))
        
        weight = start_weight - (progress * 10) + random.uniform(-0.5, 0.5) + seasonal_var
        fat = start_fat - (progress * 6) + random.uniform(-0.5, 0.5)
        
        measurements.append((
            1, d.isoformat(), 
            round(max(weight, 72), 1),  # No bajar de 72kg
            round(max(fat, 14), 1),     # No bajar de 14% grasa
            round(102 - progress * 4 + random.uniform(-0.5, 0.5), 1),  # chest
            round(90 - progress * 8 + random.uniform(-0.5, 0.5), 1),   # waist
            round(100 - progress * 4 + random.uniform(-0.5, 0.5), 1),  # hips
            round(34 + progress * 2 + random.uniform(-0.2, 0.2), 1),   # bicep_left
            round(34.5 + progress * 2 + random.uniform(-0.2, 0.2), 1), # bicep_right
            round(60 - progress * 3 + random.uniform(-0.3, 0.3), 1),   # thigh_left
            round(60.5 - progress * 3 + random.uniform(-0.3, 0.3), 1), # thigh_right
        ))
    
    for m in measurements:
        cursor.execute("""
            INSERT INTO body_measurements 
            (user_id, measurement_date, weight_kg, body_fat_percentage,
             chest_cm, waist_cm, hips_cm, bicep_left_cm, bicep_right_cm,
             thigh_left_cm, thigh_right_cm)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, m)
    conn.commit()
    print(f"✓ Insertadas {len(measurements)} mediciones corporales (1 año)")

def seed_sleep_logs(conn):
    """Inserta registros de sueño de todo el año."""
    cursor = conn.cursor()
    today = date.today()
    
    logs = []
    for i in range(365):
        d = today - timedelta(days=i)
        # Simular patrón de sueño semi-realista
        if d.weekday() in [4, 5]:  # Viernes y sábado duermen más tarde
            hours = random.uniform(5.5, 8)
            quality = random.randint(5, 8)
        elif d.weekday() == 6:  # Domingo recuperan
            hours = random.uniform(7.5, 10)
            quality = random.randint(7, 10)
        else:
            hours = random.uniform(6, 8)
            quality = random.randint(5, 9)
        
        # Vacaciones de verano y navidad duermen mejor
        if d.month in [7, 8, 12]:
            hours += random.uniform(0.5, 1)
            quality = min(10, quality + 1)
        
        logs.append((1, d.isoformat(), round(hours, 1), quality))
    
    for log in logs:
        cursor.execute("""
            INSERT INTO sleep_logs (user_id, log_date, hours_slept, sleep_quality)
            VALUES (?, ?, ?, ?)
        """, log)
    conn.commit()
    print(f"✓ Insertados {len(logs)} registros de sueño (1 año)")

def seed_step_logs(conn):
    """Inserta registros de pasos de todo el año."""
    cursor = conn.cursor()
    today = date.today()
    
    logs = []
    for i in range(365):
        d = today - timedelta(days=i)
        # Más pasos en días de entrenamiento (L, Mi, V)
        if d.weekday() in [0, 2, 4]:
            steps = random.randint(9000, 16000)
        elif d.weekday() == 6:  # Domingo más tranquilo
            steps = random.randint(2500, 6000)
        else:
            steps = random.randint(5000, 11000)
        
        # Verano más activo
        if d.month in [5, 6, 7, 8, 9]:
            steps = int(steps * random.uniform(1.1, 1.3))
        # Invierno menos activo
        elif d.month in [12, 1, 2]:
            steps = int(steps * random.uniform(0.7, 0.9))
        
        logs.append((1, d.isoformat(), steps))
    
    for log in logs:
        cursor.execute("""
            INSERT INTO step_logs (user_id, log_date, steps)
            VALUES (?, ?, ?)
        """, log)
    conn.commit()
    print(f"✓ Insertados {len(logs)} registros de pasos (1 año)")

def seed_menstrual_logs(conn):
    """Inserta registros de ciclo menstrual de todo el año."""
    cursor = conn.cursor()
    today = date.today()
    
    logs = []
    # Simular ciclos de 26-30 días durante todo el año
    cycle_start = today - timedelta(days=8)  # Último período hace 8 días
    
    for cycle in range(13):  # ~13 ciclos en un año
        cycle_length = random.randint(26, 30)
        period_start = cycle_start - timedelta(days=cycle_length * cycle)
        
        if period_start < today - timedelta(days=365):
            break
            
        # 4-6 días de período
        period_length = random.randint(4, 6)
        for day in range(period_length):
            d = period_start + timedelta(days=day)
            if d <= today and d >= today - timedelta(days=365):
                if day == 0:
                    intensity = 'light'
                elif day in [1, 2]:
                    intensity = 'heavy'
                elif day == 3:
                    intensity = 'medium'
                else:
                    intensity = 'light'
                logs.append((1, d.isoformat(), 1, intensity))
    
    for log in logs:
        cursor.execute("""
            INSERT INTO menstrual_logs (user_id, log_date, is_period_day, flow_intensity)
            VALUES (?, ?, ?, ?)
        """, log)
    conn.commit()
    print(f"✓ Insertados {len(logs)} registros menstruales (1 año)")

def seed_nutrition_goals(conn):
    """Inserta objetivos nutricionales."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO nutrition_goals 
        (user_id, calories_target, protein_target, carbs_target, fat_target, water_target_ml)
        VALUES (1, 2200, 160, 220, 70, 2500)
    """)
    conn.commit()
    print("✓ Insertados objetivos nutricionales")

def seed_food_logs(conn):
    """Inserta registros de comida de todo el año."""
    cursor = conn.cursor()
    today = date.today()
    
    # Obtener IDs de alimentos
    cursor.execute("SELECT id, name, calories FROM foods")
    foods = {row[1]: {'id': row[0], 'calories': row[2]} for row in cursor.fetchall()}
    
    # Comidas típicas por tipo
    breakfast_foods = ['Avena', 'Huevo entero', 'Pan integral', 'Plátano', 'Yogur griego', 'Leche desnatada', 'Proteína whey']
    lunch_foods = ['Pechuga de pollo', 'Arroz blanco', 'Arroz integral', 'Brócoli', 'Ensalada César', 'Pasta', 'Atún en lata', 'Patata', 'Quinoa', 'Ternera magra']
    dinner_foods = ['Salmón', 'Quinoa', 'Espinacas', 'Merluza', 'Ternera magra', 'Pavo', 'Tofu', 'Gambas', 'Calabacín', 'Pimiento rojo']
    snack_foods = ['Almendras', 'Proteína whey', 'Manzana', 'Yogur griego', 'Tortitas de arroz', 'Barrita proteica', 'Nueces', 'Plátano', 'Queso fresco batido']
    
    logs = []
    for i in range(365):  # Todo el año
        d = today - timedelta(days=i)
        
        # Algunos días no registran (simular olvidos)
        if random.random() < 0.05:
            continue
        
        # Desayuno
        available_breakfast = [f for f in breakfast_foods if f in foods]
        for food_name in random.sample(available_breakfast, min(random.randint(2, 4), len(available_breakfast))):
            quantity = random.randint(80, 150)
            logs.append((1, foods[food_name]['id'], d.isoformat(), 'breakfast', quantity))
        
        # Comida
        available_lunch = [f for f in lunch_foods if f in foods]
        for food_name in random.sample(available_lunch, min(random.randint(2, 4), len(available_lunch))):
            quantity = random.randint(100, 250)
            logs.append((1, foods[food_name]['id'], d.isoformat(), 'lunch', quantity))
        
        # Cena
        available_dinner = [f for f in dinner_foods if f in foods]
        for food_name in random.sample(available_dinner, min(random.randint(2, 3), len(available_dinner))):
            quantity = random.randint(100, 200)
            logs.append((1, foods[food_name]['id'], d.isoformat(), 'dinner', quantity))
        
        # Snacks (la mayoría de los días)
        if random.random() > 0.2:
            available_snacks = [f for f in snack_foods if f in foods]
            for food_name in random.sample(available_snacks, min(random.randint(1, 3), len(available_snacks))):
                quantity = random.randint(25, 80)
                logs.append((1, foods[food_name]['id'], d.isoformat(), 'snack', quantity))
    
    # Insertar en lotes para mayor eficiencia
    for log in logs:
        cursor.execute("""
            INSERT INTO food_logs (user_id, food_id, log_date, meal_type, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, log)
    conn.commit()
    print(f"✓ Insertados {len(logs)} registros de comida (1 año)")

def seed_water_logs(conn):
    """Inserta registros de agua de todo el año."""
    cursor = conn.cursor()
    today = date.today()
    
    logs = []
    for i in range(365):
        d = today - timedelta(days=i)
        # Más agua en verano
        if d.month in [6, 7, 8]:
            liters = round(random.uniform(2.0, 4.0), 2)
        elif d.month in [12, 1, 2]:
            liters = round(random.uniform(1.2, 2.5), 2)
        else:
            liters = round(random.uniform(1.5, 3.2), 2)
        
        # Días de entrenamiento más agua
        if d.weekday() in [0, 2, 4]:
            liters = round(liters * random.uniform(1.1, 1.3), 2)
        
        logs.append((1, d.isoformat(), liters))
    
    for log in logs:
        cursor.execute("""
            INSERT INTO water_logs (user_id, log_date, liters)
            VALUES (?, ?, ?)
        """, log)
    conn.commit()
    print(f"✓ Insertados {len(logs)} registros de agua (1 año)")

def seed_training_plan(conn):
    """Inserta un plan de entrenamiento."""
    cursor = conn.cursor()
    
    # Crear plan
    cursor.execute("""
        INSERT OR REPLACE INTO training_plans (id, user_id, name, description, is_active)
        VALUES (1, 1, 'Push Pull Legs', 'Rutina de 6 días dividida en empuje, tirón y piernas', 1)
    """)
    
    # Días de entrenamiento
    days = [
        (1, 1, 0, 'Push A - Pecho/Hombro/Tríceps'),
        (2, 1, 1, 'Pull A - Espalda/Bíceps'),
        (3, 1, 2, 'Legs A - Cuádriceps dominante'),
        (4, 1, 3, 'Push B - Hombro/Pecho/Tríceps'),
        (5, 1, 4, 'Pull B - Espalda/Bíceps'),
        (6, 1, 5, 'Legs B - Isquios dominante'),
    ]
    
    for day in days:
        cursor.execute("""
            INSERT OR REPLACE INTO training_days (id, plan_id, day_of_week, name)
            VALUES (?, ?, ?, ?)
        """, day)
    
    conn.commit()
    print("✓ Insertado plan de entrenamiento PPL")

def seed_workout_sessions(conn):
    """Inserta sesiones de entrenamiento de todo el año."""
    cursor = conn.cursor()
    today = date.today()
    
    # Obtener IDs de ejercicios por nombre
    cursor.execute("SELECT id, name FROM exercises")
    exercise_ids = {row[1]: row[0] for row in cursor.fetchall()}
    
    # Ejercicios por día
    push_exercises = ['Press banca', 'Press inclinado mancuernas', 'Aperturas mancuernas', 'Press militar', 'Elevaciones laterales', 'Extensiones en polea', 'Fondos en paralelas']
    pull_exercises = ['Dominadas', 'Remo con barra', 'Jalón al pecho', 'Remo mancuerna', 'Face pull', 'Curl con barra', 'Curl martillo', 'Curl concentrado']
    legs_exercises = ['Sentadilla', 'Prensa', 'Peso muerto rumano', 'Extensión de cuádriceps', 'Curl femoral', 'Hip thrust', 'Elevación de gemelos', 'Zancadas']
    
    session_id = 1
    sessions = []
    sets = []
    
    # Calcular días de entrenamiento (5-6 días/semana, excepto vacaciones)
    for i in range(365):
        d = today - timedelta(days=i)
        
        # No entrenar domingos
        if d.weekday() == 6:
            continue
        
        # Simular vacaciones (2 semanas en agosto, 1 en navidad)
        if (d.month == 8 and d.day >= 1 and d.day <= 14) or \
           (d.month == 12 and d.day >= 23 and d.day <= 31):
            continue
        
        # Algunos días de descanso aleatorios
        if random.random() < 0.1:
            continue
        
        day_of_week = d.weekday()
        
        if day_of_week in [0, 3]:  # Push
            day_exercises = push_exercises
        elif day_of_week in [1, 4]:  # Pull
            day_exercises = pull_exercises
        else:  # Legs
            day_exercises = legs_exercises
        
        # Crear sesión
        start_hour = random.choice([7, 8, 17, 18, 19])
        start_min = random.randint(0, 59)
        duration = random.randint(50, 80)
        end_min = start_min + duration
        end_hour = start_hour + (end_min // 60)
        end_min = end_min % 60
        
        start_time = f"{start_hour:02d}:{start_min:02d}:00"
        end_time = f"{end_hour:02d}:{end_min:02d}:00"
        
        sessions.append((session_id, 1, None, d.isoformat(), start_time, end_time))
        
        # Crear series para cada ejercicio (4-6 ejercicios por sesión)
        selected_exercises = random.sample(day_exercises, min(random.randint(4, 6), len(day_exercises)))
        
        # Progreso: ir subiendo pesos a lo largo del año
        progress = (365 - i) / 365  # 0 al inicio del año, 1 ahora
        
        for ex_name in selected_exercises:
            if ex_name in exercise_ids:
                ex_id = exercise_ids[ex_name]
                num_sets = random.randint(3, 5)
                
                # Base weight depende del ejercicio
                if 'Press banca' in ex_name or 'Sentadilla' in ex_name:
                    base_weight = 60 + progress * 30  # 60kg -> 90kg
                elif 'Peso muerto' in ex_name or 'Prensa' in ex_name:
                    base_weight = 80 + progress * 40  # 80kg -> 120kg
                elif 'Curl' in ex_name or 'Elevaciones' in ex_name:
                    base_weight = 8 + progress * 6  # 8kg -> 14kg
                else:
                    base_weight = 30 + progress * 20  # 30kg -> 50kg
                
                for set_num in range(1, num_sets + 1):
                    # Variar peso entre sets
                    weight = round(base_weight * random.uniform(0.9, 1.1), 1)
                    reps = random.randint(6, 15)
                    rpe = random.randint(7, 10)
                    sets.append((session_id, ex_id, set_num, weight, reps, rpe))
        
        session_id += 1
    
    for session in sessions:
        cursor.execute("""
            INSERT INTO workout_sessions (id, user_id, training_day_id, session_date, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, session)
    
    for s in sets:
        cursor.execute("""
            INSERT INTO workout_sets (session_id, exercise_id, set_number, weight_kg, reps, rpe)
            VALUES (?, ?, ?, ?, ?, ?)
        """, s)
    
    conn.commit()
    print(f"✓ Insertadas {len(sessions)} sesiones de entrenamiento con {len(sets)} series (1 año)")

def main():
    print("\n🏋️ Generando datos de prueba para GymGraph (1 AÑO COMPLETO)...\n")
    
    conn = get_connection()
    
    try:
        # PRIMERO: Borrar todos los datos existentes
        clear_all_data(conn)
        
        seed_foods(conn)
        seed_exercises(conn)
        seed_nutrition_goals(conn)
        seed_measurements(conn)
        seed_sleep_logs(conn)
        seed_step_logs(conn)
        seed_menstrual_logs(conn)
        seed_water_logs(conn)
        seed_food_logs(conn)
        seed_training_plan(conn)
        seed_workout_sessions(conn)
        
        print("\n✅ ¡Base de datos poblada con éxito!")
        print("\nResumen de datos generados:")
        
        # Contar registros
        cursor = conn.cursor()
        tables = ['foods', 'exercises', 'body_measurements', 'sleep_logs', 
                  'step_logs', 'menstrual_logs', 'water_logs', 'food_logs',
                  'training_plans', 'workout_sessions', 'workout_sets']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  - {table}: {count} registros")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
