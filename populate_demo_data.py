# populate_demo_data.py
import os
import sys
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

# Cargar variables de entorno
load_dotenv()

from models import Base, User, Exercise, Food, MeasCat, Meas, Objective, Trainplan, Trainday, TraindayExercise, Set, Meal, MealFood

# Configuración de la base de datos desde variable de entorno
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ Error: DATABASE_URL no está configurada en variables de entorno")
    sys.exit(1)

# Corregir SSL para Aiven
if 'ssl-mode' in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('ssl-mode', 'ssl_ca')    

def create_user(session):
    """Crear usuario de prueba"""
    
    existing_user = session.query(User).filter_by(username="user1").first()
    
    if existing_user:
        print(f"⏭️  Usuario 'user1' ya existe, saltando...")
        return existing_user.idUser
    
    user = User(
        username="user1",
        passwd=generate_password_hash("123")
    )
    session.add(user)
    session.flush()
    print(f"✅ Usuario creado: user1 (ID: {user.idUser})")
    
    return user.idUser

def create_objective(session, user_id):
    """Crear objetivo nutricional para el usuario"""
    
    existing = session.query(Objective).filter_by(User_idUser=user_id).first()
    
    if existing:
        print(f"⏭️  Objetivo ya existe para usuario {user_id}, actualizando...")
        existing.protein = 125
        existing.carbs = 313
        existing.fats = 83
        session.flush()
        return existing
    
    objective = Objective(
        protein=125,
        carbs=313,
        fats=83,
        User_idUser=user_id
    )
    session.add(objective)
    session.flush()
    print(f"✅ Objetivo creado: 2500 kcal (P:125g, C:313g, G:83g)")
    return objective

def create_trainplans(session, user_id):
    """Crear planes de entrenamiento PPL y UL"""
    
    # Obtener ejercicios de la base de datos
    exercises = {ex.name: ex.idExercise for ex in session.query(Exercise).all()}
    
    # Plan PPL (Push Pull Legs)
    ppl = Trainplan(
        name="Push Pull Legs (PPL)",
        User_idUser=user_id
    )
    session.add(ppl)
    session.flush()
    print(f"📋 Plan PPL creado con ID: {ppl.idTrainplan}")
    
    # Días para PPL (sin asignar idTrainday manualmente)
    ppl_days = [
        {"name": "Push Day", "exercises": [
            {"name": "Barbell Bench Press", "sets": 3, "notes": "8-12 reps", "order": 0},
            {"name": "Seated Dumbell Shoulder Press", "sets": 3, "notes": "8-12 reps", "order": 1},
            {"name": "Overhead Triceps Extension", "sets": 3, "notes": "10-15 reps", "order": 2}
        ]},
        {"name": "Pull Day", "exercises": [
            {"name": "Pull-Up", "sets": 3, "notes": "8-12 reps", "order": 0},
            {"name": "Bent-Over Row", "sets": 3, "notes": "8-12 reps", "order": 1},
            {"name": "EZ Barbell Preacher Curl", "sets": 3, "notes": "10-15 reps", "order": 2}
        ]},
        {"name": "Legs Day", "exercises": [
            {"name": "Hack Squat", "sets": 3, "notes": "8-12 reps", "order": 0},
            {"name": "Romanian Deadlift", "sets": 3, "notes": "8-12 reps", "order": 1},
            {"name": "Lever Hip Thrust", "sets": 3, "notes": "10-15 reps", "order": 2}
        ]}
    ]
    
    for day_data in ppl_days:
        # NO asignamos idTrainday - dejar que autoincremente
        trainday = Trainday(
            name=day_data["name"],
            Trainplan_idTrainplan=ppl.idTrainplan,
            Trainplan_User_idUser=user_id
        )
        session.add(trainday)
        session.flush()
        print(f"  - Día '{day_data['name']}' creado con ID: {trainday.idTrainday}")
        
        for ex_data in day_data["exercises"]:
            exercise_id = exercises.get(ex_data["name"])
            if exercise_id:
                tde = TraindayExercise(
                    numSets=ex_data["sets"],
                    Exercise_idExercise=exercise_id,
                    Trainday_idTrainday=trainday.idTrainday,
                    Trainday_Trainplan_idTrainplan=ppl.idTrainplan,
                    Trainday_Trainplan_User_idUser=user_id,
                    order=ex_data["order"],
                    notes=ex_data["notes"]
                )
                session.add(tde)
                print(f"    - Ejercicio añadido: {ex_data['name']}")
    
    # Plan UL (Upper Lower)
    ul = Trainplan(
        name="Upper Lower (UL)",
        User_idUser=user_id
    )
    session.add(ul)
    session.flush()
    print(f"📋 Plan UL creado con ID: {ul.idTrainplan}")
    
    # Días para UL (sin asignar idTrainday manualmente)
    ul_days = [
        {"name": "Upper Body", "exercises": [
            {"name": "Barbell Bench Press", "sets": 3, "notes": "8-12 reps", "order": 0},
            {"name": "Pull-Up", "sets": 3, "notes": "8-12 reps", "order": 1},
            {"name": "Seated Dumbell Shoulder Press", "sets": 3, "notes": "8-12 reps", "order": 2},
            {"name": "EZ Barbell Preacher Curl", "sets": 3, "notes": "10-15 reps", "order": 3},
            {"name": "Overhead Triceps Extension", "sets": 3, "notes": "10-15 reps", "order": 4}
        ]},
        {"name": "Lower Body", "exercises": [
            {"name": "Hack Squat", "sets": 3, "notes": "8-12 reps", "order": 0},
            {"name": "Romanian Deadlift", "sets": 3, "notes": "8-12 reps", "order": 1},
            {"name": "Lever Hip Thrust", "sets": 3, "notes": "10-15 reps", "order": 2}
        ]}
    ]
    
    for day_data in ul_days:
        # NO asignamos idTrainday - dejar que autoincremente
        trainday = Trainday(
            name=day_data["name"],
            Trainplan_idTrainplan=ul.idTrainplan,
            Trainplan_User_idUser=user_id
        )
        session.add(trainday)
        session.flush()
        print(f"  - Día '{day_data['name']}' creado con ID: {trainday.idTrainday}")
        
        for ex_data in day_data["exercises"]:
            exercise_id = exercises.get(ex_data["name"])
            if exercise_id:
                tde = TraindayExercise(
                    numSets=ex_data["sets"],
                    Exercise_idExercise=exercise_id,
                    Trainday_idTrainday=trainday.idTrainday,
                    Trainday_Trainplan_idTrainplan=ul.idTrainplan,
                    Trainday_Trainplan_User_idUser=user_id,
                    order=ex_data["order"],
                    notes=ex_data["notes"]
                )
                session.add(tde)
                print(f"    - Ejercicio añadido: {ex_data['name']}")
    
    session.flush()
    print(f"✅ Planes creados exitosamente")
    return ppl.idTrainplan, ul.idTrainplan

def generate_workout_data(session, user_id, start_date, end_date):
    """Generar datos de entrenamiento para 3 meses (3 veces por semana)"""
    
    # Obtener traindays de los planes
    traindays = session.query(Trainday).filter(Trainday.Trainplan_User_idUser == user_id).all()
    trainday_dict = {td.name: td for td in traindays}
    
    # Días de entrenamiento (Lunes, Miércoles, Viernes)
    workout_days = []
    current = start_date
    while current <= end_date:
        if current.weekday() in [0, 2, 4]:  # Lunes, Miércoles, Viernes
            workout_days.append(current)
        current += timedelta(days=1)
    
    print(f"📊 Generando {len(workout_days)} sesiones de entrenamiento...")
    
    sets_created = 0
    next_set_id = 1
    
    # Obtener el máximo idSet actual para continuar desde ahí
    max_id = session.query(Set.idSet).order_by(Set.idSet.desc()).first()
    if max_id:
        next_set_id = max_id[0] + 1
    
    for i, date in enumerate(workout_days):
        # Alternar entre planes PPL y UL
        plan_type = i % 2  # 0 = PPL, 1 = UL
        day_of_week = date.weekday()
        
        # Seleccionar trainday según el día
        if plan_type == 0:  # PPL
            if day_of_week == 0:  # Lunes - Push
                day_name = "Push Day"
            elif day_of_week == 2:  # Miércoles - Pull
                day_name = "Pull Day"
            else:  # Viernes - Legs
                day_name = "Legs Day"
        else:  # UL
            if day_of_week in [0, 2]:  # Lunes o Miércoles - Upper
                day_name = "Upper Body"
            else:  # Viernes - Lower
                day_name = "Lower Body"
        
        # Buscar el trainday correspondiente
        trainday = trainday_dict.get(day_name)
        
        if trainday:
            # Obtener ejercicios del trainday
            tdes = session.query(TraindayExercise).filter(
                TraindayExercise.Trainday_idTrainday == trainday.idTrainday,
                TraindayExercise.Trainday_Trainplan_User_idUser == user_id
            ).all()
            
            for tde in tdes:
                # Para cada ejercicio, generar series
                for set_num in range(tde.numSets):
                    # Progresión: aumentar peso/repeticiones con el tiempo
                    week = (date - start_date).days // 7
                    base_weight = random.uniform(40, 80)
                    progress = week * 0.5  # Aumento de 0.5kg por semana
                    
                    weight = round(base_weight + progress, 1)
                    reps = random.randint(8, 12)
                    
                    # Asignar idSet manualmente
                    workout_set = Set(
                        idSet=next_set_id,
                        weight=weight,
                        reps=reps,
                        date=datetime.combine(date, datetime.min.time()),
                        Exercise_idExercise=tde.Exercise_idExercise,
                        User_idUser=user_id
                    )
                    session.add(workout_set)
                    next_set_id += 1
                    sets_created += 1
        
        # Commit cada 10 días para no saturar
        if i % 10 == 0 and i > 0:
            session.flush()
            print(f"  - Procesados {i} días, {sets_created} series...")
    
    session.flush()
    print(f"✅ Datos de entrenamiento generados: {sets_created} series")

def generate_meal_data(session, user_id, foods, start_date, end_date):
    """Generar datos de comidas para 3 meses (todos los días)"""
    
    if not foods:
        print("⚠️  No hay alimentos, saltando generación de comidas...")
        return
    
    meals_created = 0
    foods_created = 0
    
    # Obtener el máximo idMeal actual para continuar desde ahí
    max_id = session.query(Meal.idMeal).order_by(Meal.idMeal.desc()).first()
    next_meal_id = 1
    if max_id:
        next_meal_id = max_id[0] + 1
    
    current = start_date
    while current <= end_date:
        # Crear 3 comidas por día (desayuno, almuerzo, cena) con diferentes horas
        meal_times = [
            {"hour": 8, "minute": 30},   # Desayuno 8:30
            {"hour": 13, "minute": 0},   # Almuerzo 13:00
            {"hour": 20, "minute": 30}   # Cena 20:30
        ]
        
        for meal_time in meal_times:
            # Crear datetime con fecha y hora
            meal_datetime = datetime.combine(current, datetime.min.time())
            meal_datetime = meal_datetime.replace(hour=meal_time["hour"], minute=meal_time["minute"])
            
            # Guardar como string en el formato que usa la app
            # La app usa 'YYYY-MM-DD HH:MM:SS'
            date_str = meal_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
            meal = Meal(
                idMeal=next_meal_id,
                date=date_str,
                User_idUser=user_id
            )
            session.add(meal)
            next_meal_id += 1
            session.flush()
            
            # Añadir 2-4 alimentos por comida
            num_foods = random.randint(2, 4)
            selected_foods = random.sample(foods, min(num_foods, len(foods)))
            
            for food in selected_foods:
                grams = random.randint(50, 200)
                meal_food = MealFood(
                    grams=grams,
                    Food_idFood=food.idFood,
                    Meal_idMeal=meal.idMeal,
                    Meal_User_idUser=user_id
                )
                session.add(meal_food)
                foods_created += 1
            
            meals_created += 1
        
        current += timedelta(days=1)
        
        # Commit cada 10 días
        if (current - start_date).days % 10 == 0:
            session.flush()
    
    session.flush()
    print(f"✅ Datos de comidas generados: {meals_created} comidas, {foods_created} alimentos")

def populate_foods(session, user_id):
    """Rellena la tabla Food con alimentos base para el usuario"""
    
    foods_data = [
        {"name": "Chicken Breast", "protein_p100": 31.0, "carbs_p100": 0.0, "fats_p100": 3.6, "kcal_p100": 165},
        {"name": "White Rice", "protein_p100": 2.7, "carbs_p100": 28.0, "fats_p100": 0.3, "kcal_p100": 130},
        {"name": "Oats", "protein_p100": 13.0, "carbs_p100": 68.0, "fats_p100": 7.0, "kcal_p100": 389},
        {"name": "Eggs", "protein_p100": 13.0, "carbs_p100": 1.1, "fats_p100": 11.0, "kcal_p100": 155},
        {"name": "Salmon", "protein_p100": 22.0, "carbs_p100": 0.0, "fats_p100": 13.0, "kcal_p100": 208},
        {"name": "Broccoli", "protein_p100": 2.8, "carbs_p100": 7.0, "fats_p100": 0.4, "kcal_p100": 34},
        {"name": "Almonds", "protein_p100": 21.0, "carbs_p100": 22.0, "fats_p100": 49.0, "kcal_p100": 579},
        {"name": "Greek Yogurt", "protein_p100": 10.0, "carbs_p100": 4.0, "fats_p100": 0.4, "kcal_p100": 59},
        {"name": "Sweet Potato", "protein_p100": 1.6, "carbs_p100": 20.0, "fats_p100": 0.1, "kcal_p100": 86},
        {"name": "Avocado", "protein_p100": 2.0, "carbs_p100": 9.0, "fats_p100": 15.0, "kcal_p100": 160},
        {"name": "Beef Steak", "protein_p100": 26.0, "carbs_p100": 0.0, "fats_p100": 17.0, "kcal_p100": 250},
        {"name": "Quinoa", "protein_p100": 4.4, "carbs_p100": 21.0, "fats_p100": 1.9, "kcal_p100": 120},
        {"name": "Tuna", "protein_p100": 30.0, "carbs_p100": 0.0, "fats_p100": 0.6, "kcal_p100": 132},
        {"name": "Spinach", "protein_p100": 2.9, "carbs_p100": 3.6, "fats_p100": 0.4, "kcal_p100": 23},
        {"name": "Olive Oil", "protein_p100": 0.0, "carbs_p100": 0.0, "fats_p100": 100.0, "kcal_p100": 884}
    ]
    
    foods_added = 0
    foods_skipped = 0
    
    for data in foods_data:
        # Verificar si el alimento ya existe para este usuario
        existing = session.query(Food).filter_by(
            name=data["name"], 
            User_idUser=user_id
        ).first()
        
        if existing:
            print(f"⏭️  Alimento '{data['name']}' ya existe, saltando...")
            foods_skipped += 1
            continue
        
        # Crear nuevo alimento
        food = Food(
            name=data["name"],
            protein_p100=data["protein_p100"],
            carbs_p100=data["carbs_p100"],
            fats_p100=data["fats_p100"],
            kcal_p100=data["kcal_p100"],
            User_idUser=user_id
        )
        session.add(food)
        foods_added += 1
        print(f"✅ Alimento añadido: {data['name']} (P:{data['protein_p100']}g, C:{data['carbs_p100']}g, G:{data['fats_p100']}g, {data['kcal_p100']}kcal/100g)")
    
    session.flush()
    print(f"\n📊 Resumen Foods: {foods_added} añadidos, {foods_skipped} existentes")
    return foods_added

def generate_measurements(session, user_id, start_date, end_date):
    """Generar mediciones semanales para 3 meses"""
    
    measurements_created = 0
    
    # Obtener categorías de medición
    categories = session.query(MeasCat).all()
    
    # Obtener el máximo idMeas actual para continuar desde ahí
    max_id = session.query(Meas.idMeas).order_by(Meas.idMeas.desc()).first()
    next_meas_id = 1
    if max_id:
        next_meas_id = max_id[0] + 1
    
    # Mediciones cada semana
    current = start_date
    week = 0
    base_weight = 75.0
    
    while current <= end_date:
        if current.weekday() == 0:  # Lunes de cada semana
            for cat in categories:
                if cat.name == "Body weight":
                    # Progresión de peso: disminuye ligeramente con el tiempo
                    value = base_weight - (week * 0.2) + random.uniform(-0.5, 0.5)
                    value = round(max(60, min(90, value)), 1)
                
                elif cat.name == "Water intake":
                    # Agua: entre 2000 y 3500 ml, representado como litros (2.0 a 3.5)
                    value = random.uniform(2.0, 3.5)
                    value = round(value, 1)
                
                elif cat.name == "Sleep hours":
                    value = random.uniform(6.5, 8.5)
                    value = round(value, 1)
                
                elif cat.name == "Menstruation":
                    # Menstruación: cada 4 semanas, valor entre 1-5
                    if week > 0 and week % 4 == 0:
                        value = random.randint(1, 5)
                    else:
                        value = 0
                
                else:
                    # Mediciones corporales con variación aleatoria
                    if cat.name == "Shoulders":
                        value = 110 + random.uniform(-2, 2) - (week * 0.1)
                    elif cat.name == "Chest":
                        value = 95 + random.uniform(-2, 2) - (week * 0.1)
                    elif "bicep" in cat.name.lower():
                        value = 32 + random.uniform(-1, 1) + (week * 0.05)
                    elif "forearm" in cat.name.lower():
                        value = 28 + random.uniform(-1, 1) + (week * 0.03)
                    elif cat.name == "Waist":
                        value = 80 - (week * 0.3) + random.uniform(-1, 1)
                    elif cat.name == "Hips":
                        value = 95 - (week * 0.2) + random.uniform(-1, 1)
                    elif "thigh" in cat.name.lower():
                        value = 55 + random.uniform(-1, 1) - (week * 0.05)
                    elif "calf" in cat.name.lower():
                        value = 36 + random.uniform(-1, 1) - (week * 0.03)
                    else:
                        value = random.uniform(30, 40)
                    
                    value = round(value, 1)
                
                # Saltar valores no válidos
                if cat.name == "Menstruation" and value == 0:
                    continue
                
                # Asegurar que el valor no exceda el límite de DECIMAL(5,2)
                if value > 999.99:
                    value = 999.99
                elif value < 0:
                    value = 0
                
                # Asignar idMeas manualmente
                measurement = Meas(
                    idMeas=next_meas_id,
                    val=value,
                    date=datetime.combine(current, datetime.min.time()),
                    MeasCat_idMeasCat=cat.idMeasCat,
                    User_idUser=user_id
                )
                session.add(measurement)
                next_meas_id += 1
                measurements_created += 1
            
            week += 1
        
        current += timedelta(days=1)
    
    session.flush()
    print(f"✅ Mediciones generadas: {measurements_created} registros")

def main():
    """Función principal del script"""
    
    print("=" * 60)
    print("🚀 Iniciando script de población de datos demo")
    print("=" * 60)
    
    try:
        # Crear conexión a la base de datos
        engine = create_engine(DATABASE_URL, echo=False)
        
        # Crear las tablas si no existen
        Base.metadata.create_all(engine)
        print("✅ Tablas verificadas/creadas correctamente")
        
        # Crear sesión
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # 1. Crear usuario
        print("\n" + "=" * 60)
        print("📋 Creando usuario de prueba...")
        print("=" * 60)
        user_id = create_user(session)
        
        # 2. Crear objetivo nutricional
        print("\n" + "=" * 60)
        print("📋 Creando objetivo nutricional...")
        print("=" * 60)
        create_objective(session, user_id)
        
        # 3. Crear alimentos base para el usuario
        print("\n" + "=" * 60)
        print("📋 Creando alimentos base...")
        print("=" * 60)
        foods_count = populate_foods(session, user_id)
        
        # 4. Obtener alimentos para usar en comidas
        foods = session.query(Food).filter(Food.User_idUser == user_id).all()
        
        # 5. Crear planes de entrenamiento
        print("\n" + "=" * 60)
        print("📋 Creando planes de entrenamiento...")
        print("=" * 60)
        create_trainplans(session, user_id)
        
        # 6. Generar datos históricos (3 meses atrás hasta hoy)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=90)  # 3 meses
        
        print("\n" + "=" * 60)
        print(f"📋 Generando datos históricos ({start_date} a {end_date})...")
        print("=" * 60)
        
        # Generar datos de entrenamiento
        generate_workout_data(session, user_id, start_date, end_date)
        
        # Generar datos de comidas (solo si hay alimentos)
        if foods:
            generate_meal_data(session, user_id, foods, start_date, end_date)
        else:
            print("⚠️  No se pudieron crear alimentos, saltando generación de comidas...")
        
        # Generar mediciones
        generate_measurements(session, user_id, start_date, end_date)
        
        # Commit final
        session.commit()
        
        print("\n" + "=" * 60)
        print("🎉 Script completado exitosamente!")
        print("=" * 60)
        print(f"\n📊 Resumen:")
        print(f"   - Usuario: user1 (contraseña: 123)")
        print(f"   - Alimentos: {foods_count} alimentos base")
        print(f"   - Período: {start_date} a {end_date}")
        print(f"   - Entrenamientos: 3 veces por semana")
        print(f"   - Planes: PPL y UL")
        print(f"   - Mediciones: semanales")
        
        # Cerrar sesión
        session.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()