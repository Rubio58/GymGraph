# populate_tables.py
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Exercise, MeasCat

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos desde variable de entorno
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ Error: DATABASE_URL no está configurada en variables de entorno")
    sys.exit(1)

if not DATABASE_URL:
    print("❌ Error: DATABASE_URL no está configurada en variables de entorno")
    sys.exit(1)
    
def populate_exercises(session):
    """Rellena la tabla Exercise con los ejercicios proporcionados"""
    
    exercises_data = [
        {"name": "Pull-Up", "musclegroup": "Lats"},
        {"name": "Bent-Over Row", "musclegroup": "Traps"},
        {"name": "Barbell Bench Press", "musclegroup": "Chest"},
        {"name": "EZ Barbell Preacher Curl", "musclegroup": "Biceps"},
        {"name": "Romanian Deadlift", "musclegroup": "Hamstrings"},
        {"name": "Dumbell Lateral Raises", "musclegroup": "Side Delts"},
        {"name": "Hack Squat", "musclegroup": "Quads"},
        {"name": "Overhead Triceps Extension", "musclegroup": "Triceps"},
        {"name": "Seated Dumbell Shoulder Press", "musclegroup": "Front Delts"},
        {"name": "Lever Hip Thrust", "musclegroup": "Glutes"}
    ]
    
    exercises_added = 0
    exercises_skipped = 0
    
    for data in exercises_data:
        # Verificar si el ejercicio ya existe
        existing = session.query(Exercise).filter_by(name=data["name"]).first()
        
        if existing:
            print(f"⏭️  Ejercicio '{data['name']}' ya existe, saltando...")
            exercises_skipped += 1
            continue
        
        # Crear nuevo ejercicio
        exercise = Exercise(
            name=data["name"],
            musclegroup=data["musclegroup"]
        )
        session.add(exercise)
        exercises_added += 1
        print(f"✅ Ejercicio añadido: {data['name']} ({data['musclegroup']})")
    
    session.commit()
    print(f"\n📊 Resumen Exercises: {exercises_added} añadidos, {exercises_skipped} existentes")

def populate_meas_cat(session):
    """Rellena la tabla MeasCat con las categorías proporcionadas"""
    
    meas_cat_data = [
        {"name": "Body weight", "unit": "kg"},
        {"name": "Shoulders", "unit": "cm"},
        {"name": "Chest", "unit": "cm"},
        {"name": "Left bicep", "unit": "cm"},
        {"name": "Right bicep", "unit": "cm"},
        {"name": "Left forearm", "unit": "cm"},
        {"name": "Right forearm", "unit": "cm"},
        {"name": "Waist", "unit": "cm"},
        {"name": "Hips", "unit": "cm"},
        {"name": "Left thigh", "unit": "cm"},
        {"name": "Right thigh", "unit": "cm"},
        {"name": "Left calf", "unit": "cm"},
        {"name": "Right calf", "unit": "cm"},
        {"name": "Menstruation", "unit": "flow"},
        {"name": "Water intake", "unit": "ml"},
        {"name": "Sleep hours", "unit": "h"}
    ]
    
    categories_added = 0
    categories_skipped = 0
    
    for data in meas_cat_data:
        # Verificar si la categoría ya existe
        existing = session.query(MeasCat).filter_by(name=data["name"]).first()
        
        if existing:
            print(f"⏭️  Categoría '{data['name']}' ya existe, saltando...")
            categories_skipped += 1
            continue
        
        # Crear nueva categoría
        meas_cat = MeasCat(
            name=data["name"],
            unit=data["unit"]
        )
        session.add(meas_cat)
        categories_added += 1
        print(f"✅ Categoría añadida: {data['name']} ({data['unit']})")
    
    session.commit()
    print(f"\n📊 Resumen MeasCat: {categories_added} añadidas, {categories_skipped} existentes")


def main():
    """Función principal del script"""
    
    print("=" * 60)
    print("🚀 Iniciando script de población de tablas")
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
        
        # Poblar tablas
        print("\n" + "=" * 60)
        print("📋 Poblando tabla Exercise...")
        print("=" * 60)
        populate_exercises(session)
        
        print("\n" + "=" * 60)
        print("📋 Poblando tabla MeasCat...")
        print("=" * 60)
        populate_meas_cat(session)
        
        # Cerrar sesión
        session.close()
        
        print("\n" + "=" * 60)
        print("🎉 Script completado exitosamente!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()