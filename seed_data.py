"""
Script para rellenar la BD con datos de prueba realistas (90 días).
Ejecutar: python3 seed_data.py
"""
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from database import engine

random.seed(42)

def trend(day, start, end, noise=0.0):
    val = start + (end - start) * (day / 89)
    return round(val + random.gauss(0, noise), 2)

def skip_day(prob=0.15):
    return random.random() < prob

def seed():
    with engine.begin() as conn:

        # ── Limpiar usuario demo si existe ───────────────────────────────────
        row = conn.execute(text("SELECT idUser FROM User WHERE username = 'demo'")).fetchone()
        if row:
            uid_old = row[0]
            # Borrar en orden de dependencias
            conn.execute(text(f"DELETE FROM `Set` WHERE User_idUser = {uid_old}"))
            conn.execute(text(f"DELETE te FROM `Trainday_exercise` te JOIN `Trainday` td ON te.Trainday_idTrainday = td.idTrainday JOIN `Trainplan` tp ON td.Trainplan_idTrainplan = tp.idTrainplan WHERE tp.User_idUser = {uid_old}"))
            conn.execute(text(f"DELETE td FROM `Trainday` td JOIN `Trainplan` tp ON td.Trainplan_idTrainplan = tp.idTrainplan WHERE tp.User_idUser = {uid_old}"))
            conn.execute(text(f"DELETE FROM `Trainplan` WHERE User_idUser = {uid_old}"))
            conn.execute(text(f"DELETE mf FROM `Meal_Food` mf JOIN `Meal` m ON mf.Meal_idMeal = m.idMeal WHERE m.User_idUser = {uid_old}"))
            conn.execute(text(f"DELETE FROM `Meal` WHERE User_idUser = {uid_old}"))
            conn.execute(text(f"DELETE FROM `Food` WHERE User_idUser = {uid_old}"))
            conn.execute(text(f"DELETE FROM `Meas` WHERE User_idUser = {uid_old}"))
            conn.execute(text(f"DELETE FROM `Objective` WHERE User_idUser = {uid_old}"))
            conn.execute(text(f"DELETE FROM `User` WHERE idUser = {uid_old}"))

        # ── Usuario ──────────────────────────────────────────────────────────
        passwd = generate_password_hash('demo1234')
        conn.execute(text(f"INSERT INTO User (username, passwd) VALUES ('demo', '{passwd}')"))
        uid = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()

        # ── Objetivo ─────────────────────────────────────────────────────────
        conn.execute(text(f"INSERT INTO Objective (idObjective, Protein, Carbs, Fats, User_idUser) VALUES (1, 160, 300, 70, {uid})"))

        # ── Categorías de medidas ─────────────────────────────────────────────
        for cat_id, name, unit in [(1, 'Body Weight', 'kg'), (2, 'Body Fat', '%'), (3, 'Waist', 'cm')]:
            exists = conn.execute(text(f"SELECT 1 FROM MeasCat WHERE idMeasCat = {cat_id}")).fetchone()
            if not exists:
                conn.execute(text(f"INSERT INTO MeasCat (idMeasCat, name, unit) VALUES ({cat_id}, '{name}', '{unit}')"))

        # ── Alimentos ────────────────────────────────────────────────────────
        foods = [
            (1, 'Pechuga de pollo', 31.0, 0.0, 3.6, 165),
            (2, 'Arroz blanco cocido', 2.7, 28.0, 0.3, 130),
            (3, 'Huevo entero', 13.0, 1.1, 11.0, 155),
            (4, 'Avena', 13.0, 66.0, 7.0, 389),
            (5, 'Atún en lata', 25.0, 0.0, 1.0, 116),
            (6, 'Plátano', 1.1, 23.0, 0.3, 96),
            (7, 'Brócoli', 2.8, 7.0, 0.4, 35),
            (8, 'Aceite de oliva', 0.0, 0.0, 100.0, 884),
            (9, 'Queso cottage', 11.0, 3.4, 4.3, 98),
            (10, 'Batata', 1.6, 20.0, 0.1, 86),
        ]
        for fid, fname, prot, carbs, fats, kcal in foods:
            conn.execute(text(
                f"INSERT INTO Food (idFood, name, protein_p100, carbs_p100, fats_p100, kcal_p100, User_idUser) "
                f"VALUES ({fid}, '{fname}', {prot}, {carbs}, {fats}, {kcal}, {uid})"
            ))

        # ── Ejercicios ───────────────────────────────────────────────────────
        exercises = [
            (1, 'Sentadilla', 'Piernas'), (2, 'Press de banca', 'Pecho'),
            (3, 'Peso muerto', 'Espalda'), (4, 'Press militar', 'Hombros'),
            (5, 'Dominadas', 'Espalda'), (6, 'Curl de bíceps', 'Bíceps'),
            (7, 'Extensión tríceps', 'Tríceps'), (8, 'Zancadas', 'Piernas'),
            (9, 'Remo con barra', 'Espalda'), (10, 'Hip thrust', 'Glúteos'),
        ]
        for eid, ename, egroup in exercises:
            exists = conn.execute(text(f"SELECT 1 FROM Exercise WHERE idExercise = {eid}")).fetchone()
            if not exists:
                conn.execute(text(f"INSERT INTO Exercise (idExercise, name, musclegroup) VALUES ({eid}, '{ename}', '{egroup}')"))

        # ── Plan de entrenamiento ────────────────────────────────────────────
        conn.execute(text(f"INSERT INTO Trainplan (idTrainplan, name, User_idUser) VALUES (1, 'Fullbody 3x semana', {uid})"))

        days_cfg = [
            (1, 'Día A - Empuje', [(2, 1), (4, 2), (7, 3)]),
            (2, 'Día B - Tirón',  [(3, 1), (5, 2), (9, 3), (6, 4)]),
            (3, 'Día C - Piernas', [(1, 1), (8, 2), (10, 3)]),
        ]
        tde_map = {}  # (td_id, ex_id) -> idTrainday_exercise
        for td_id, td_name, exs in days_cfg:
            conn.execute(text(f"INSERT INTO Trainday (idTrainday, name, Trainplan_idTrainplan, Trainplan_User_idUser) VALUES ({td_id}, '{td_name}', 1, {uid})"))
            for ex_id, order in exs:
                conn.execute(text(
                    f"INSERT INTO Trainday_exercise (Exercise_idExercise, Trainday_idTrainday, Trainday_Trainplan_idTrainplan, Trainday_Trainplan_User_idUser, numSets, `order`, notes) "
                    f"VALUES ({ex_id}, {td_id}, 1, {uid}, 3, {order}, NULL)"
                ))
                tde_id = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()
                tde_map[(td_id, ex_id)] = tde_id

        # ── 90 días de datos ─────────────────────────────────────────────────
        today = datetime.now().date()
        base_date = today - timedelta(days=89)

        base_weights = {1:80, 2:70, 3:100, 4:40, 5:0, 6:15, 7:25, 8:20, 9:60, 10:80}
        end_weights  = {1:95, 2:82, 3:118, 4:50, 5:0, 6:20, 7:32, 8:30, 9:72, 10:95}
        workout_pattern = {0: 1, 2: 2, 4: 3}  # lunes=A, miércoles=B, viernes=C

        meal_id = 1
        mf_id = 1
        set_id = 1
        meas_id = 1

        for day_offset in range(90):
            current_date = base_date + timedelta(days=day_offset)
            date_str = current_date.strftime('%Y-%m-%d')
            weekday = current_date.weekday()

            # Comidas
            if not skip_day(0.05):
                cf = 1.0 + 0.12 * (day_offset / 89) + random.gauss(0, 0.05)

                # Almuerzo
                conn.execute(text(f"INSERT INTO Meal (idMeal, date, User_idUser) VALUES ({meal_id}, '{date_str}', {uid})"))
                for food_id, base_g in [(1, 150), (2, 200), (3, 50)]:
                    g = round(base_g * cf + random.gauss(0, 15), 1)
                    conn.execute(text(f"INSERT INTO Meal_Food (idMeal_Food, grams, Food_idFood, Meal_idMeal, Meal_User_idUser) VALUES ({mf_id}, {g}, {food_id}, {meal_id}, {uid})"))
                    mf_id += 1
                meal_id += 1

                # Cena
                conn.execute(text(f"INSERT INTO Meal (idMeal, date, User_idUser) VALUES ({meal_id}, '{date_str}', {uid})"))
                for food_id, base_g in [(5, 120), (10, 180), (7, 100)]:
                    g = round(base_g * cf + random.gauss(0, 12), 1)
                    conn.execute(text(f"INSERT INTO Meal_Food (idMeal_Food, grams, Food_idFood, Meal_idMeal, Meal_User_idUser) VALUES ({mf_id}, {g}, {food_id}, {meal_id}, {uid})"))
                    mf_id += 1
                meal_id += 1

            # Entrenamiento
            if weekday in workout_pattern and not skip_day(0.08):
                td_id = workout_pattern[weekday]
                day_cfg = next(d for d in days_cfg if d[0] == td_id)
                deload = 0.9 if (day_offset // 7) % 4 == 3 else 1.0

                for ex_id, _ in day_cfg[2]:
                    tde_id = tde_map.get((td_id, ex_id))
                    if not tde_id:
                        continue
                    w = trend(day_offset, base_weights[ex_id], end_weights[ex_id], noise=2) * deload
                    w = max(w, 5)
                    for s in range(3):
                        weight_val = round(w - s * random.uniform(0, 2.5), 2)
                        reps = random.randint(4, 10) if ex_id == 5 else random.randint(6, 12)
                        dt_str = datetime.combine(current_date, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S')
                        conn.execute(text(
                            f"INSERT INTO `Set` (idSet, weight, reps, date, Exercise_idExercise, User_idUser) "
                            f"VALUES ({set_id}, {weight_val}, {reps}, '{dt_str}', {ex_id}, {uid})"
                        ))
                        set_id += 1

            # Medidas (lunes y jueves)
            if weekday in (0, 3) and not skip_day(0.2):
                for cat_id, s, e, noise in [(1, 88.0, 84.0, 0.6), (2, 18.0, 15.0, 0.4), (3, 87.0, 83.0, 0.5)]:
                    val = trend(day_offset, s, e, noise)
                    conn.execute(text(
                        f"INSERT INTO Meas (idMeas, val, date, MeasCat_idMeasCat, User_idUser) "
                        f"VALUES ({meas_id}, {val}, '{date_str}', {cat_id}, {uid})"
                    ))
                    meas_id += 1

        print(f"✓ Seed completado.")
        print(f"  Usuario: demo / demo1234")
        print(f"  Días: 90 ({base_date} → {today})")
        print(f"  Comidas (registros Meal): ~{meal_id}")
        print(f"  Sets de entrenamiento: ~{set_id}")
        print(f"  Medidas corporales: ~{meas_id}")

if __name__ == '__main__':
    seed()

