# services/dashboard_service.py
from database import get_db
from sqlalchemy import text
from datetime import datetime, timedelta

class DashboardService:
    """Servicio para obtener datos de las gráficas del dashboard"""

    def get_macros_last_days(self, user_id: int, days: int = 7) -> dict:
        """Macros consumidos por día en los últimos N días"""
        with get_db() as db:
            query = text("""
                SELECT DATE(m.date) AS dia,
                       COALESCE(SUM(f.protein_p100 * mf.grams / 100), 0) AS protein,
                       COALESCE(SUM(f.carbs_p100 * mf.grams / 100), 0) AS carbs,
                       COALESCE(SUM(f.fats_p100 * mf.grams / 100), 0) AS fats,
                       COALESCE(SUM(f.kcal_p100 * mf.grams / 100), 0) AS kcal
                FROM Meal m
                JOIN Meal_Food mf ON m.idMeal = mf.Meal_idMeal
                JOIN Food f ON mf.Food_idFood = f.idFood
                WHERE m.User_idUser = :user_id
                  AND DATE(m.date) >= DATE_SUB(CURDATE(), INTERVAL :days DAY)
                GROUP BY DATE(m.date)
                ORDER BY dia
            """)
            rows = db.execute(query, {"user_id": user_id, "days": days}).fetchall()

            labels = []
            protein = []
            carbs = []
            fats = []
            kcal = []
            for r in rows:
                labels.append(str(r[0]))
                protein.append(round(float(r[1]), 1))
                carbs.append(round(float(r[2]), 1))
                fats.append(round(float(r[3]), 1))
                kcal.append(round(float(r[4]), 1))

            return {
                "labels": labels,
                "protein": protein,
                "carbs": carbs,
                "fats": fats,
                "kcal": kcal
            }

    def get_weight_progress(self, user_id: int) -> dict:
        """Evolución del peso máximo por ejercicio a lo largo del tiempo"""
        with get_db() as db:
            query = text("""
                SELECT DATE(s.date) AS dia,
                       e.name AS exercise,
                       MAX(s.weight) AS max_weight
                FROM `Set` s
                JOIN Trainday_exercise te
                  ON s.Trainday_exercise_idTrainday_exercise = te.idTrainday_exercise
                JOIN Trainday td
                  ON te.Trainday_idTrainday = td.idTrainday
                JOIN Trainplan tp
                  ON td.Trainplan_idTrainplan = tp.idTrainplan
                JOIN Exercise e
                  ON te.Exercise_idExercise = e.idExercise
                WHERE tp.User_idUser = :user_id
                GROUP BY DATE(s.date), e.name
                ORDER BY dia
            """)
            rows = db.execute(query, {"user_id": user_id}).fetchall()

            # Agrupar por ejercicio
            exercises = {}
            all_dates = set()
            for r in rows:
                date_str = str(r[0])
                exercise = r[1]
                weight = float(r[2])
                all_dates.add(date_str)
                if exercise not in exercises:
                    exercises[exercise] = {}
                exercises[exercise][date_str] = weight

            labels = sorted(all_dates)
            datasets = []
            for ex_name, date_weights in exercises.items():
                data = [date_weights.get(d, None) for d in labels]
                datasets.append({"label": ex_name, "data": data})

            return {"labels": labels, "datasets": datasets}

    def get_muscle_distribution(self, user_id: int) -> dict:
        """Distribución de ejercicios por grupo muscular"""
        with get_db() as db:
            query = text("""
                SELECT e.musclegroup, COUNT(*) AS total
                FROM Trainday_exercise te
                JOIN Trainday td ON te.Trainday_idTrainday = td.idTrainday
                JOIN Trainplan tp ON td.Trainplan_idTrainplan = tp.idTrainplan
                JOIN Exercise e ON te.Exercise_idExercise = e.idExercise
                WHERE tp.User_idUser = :user_id
                GROUP BY e.musclegroup
                ORDER BY total DESC
            """)
            rows = db.execute(query, {"user_id": user_id}).fetchall()

            labels = [r[0] for r in rows]
            data = [int(r[1]) for r in rows]

            return {"labels": labels, "data": data}

    def get_volume_per_session(self, user_id: int) -> dict:
        """Volumen total (peso x reps) por sesión"""
        with get_db() as db:
            query = text("""
                SELECT DATE(s.date) AS dia,
                       SUM(s.weight * s.reps) AS volumen
                FROM `Set` s
                JOIN Trainday_exercise te
                  ON s.Trainday_exercise_idTrainday_exercise = te.idTrainday_exercise
                JOIN Trainday td
                  ON te.Trainday_idTrainday = td.idTrainday
                JOIN Trainplan tp
                  ON td.Trainplan_idTrainplan = tp.idTrainplan
                WHERE tp.User_idUser = :user_id
                GROUP BY DATE(s.date)
                ORDER BY dia
            """)
            rows = db.execute(query, {"user_id": user_id}).fetchall()

            labels = [str(r[0]) for r in rows]
            data = [round(float(r[1]), 1) for r in rows]

            return {"labels": labels, "data": data}

    def get_today_macros_vs_objective(self, user_id: int) -> dict:
        """Macros consumidos hoy vs objetivo del usuario"""
        with get_db() as db:
            # Objetivo
            obj_query = text("""
                SELECT Protein, Carbs, Fats FROM Objective
                WHERE User_idUser = :user_id
                LIMIT 1
            """)
            obj = db.execute(obj_query, {"user_id": user_id}).fetchone()

            # Consumido hoy
            cons_query = text("""
                SELECT COALESCE(SUM(f.protein_p100 * mf.grams / 100), 0),
                       COALESCE(SUM(f.carbs_p100 * mf.grams / 100), 0),
                       COALESCE(SUM(f.fats_p100 * mf.grams / 100), 0)
                FROM Meal m
                JOIN Meal_Food mf ON m.idMeal = mf.Meal_idMeal
                JOIN Food f ON mf.Food_idFood = f.idFood
                WHERE m.User_idUser = :user_id
                  AND DATE(m.date) = CURDATE()
            """)
            cons = db.execute(cons_query, {"user_id": user_id}).fetchone()

            return {
                "objetivo": {
                    "protein": int(obj[0]) if obj else 0,
                    "carbs": int(obj[1]) if obj else 0,
                    "fats": int(obj[2]) if obj else 0,
                },
                "consumido": {
                    "protein": round(float(cons[0]), 1) if cons else 0,
                    "carbs": round(float(cons[1]), 1) if cons else 0,
                    "fats": round(float(cons[2]), 1) if cons else 0,
                }
            }

    def get_last_workout(self, user_id: int) -> dict:
        """Datos del último entrenamiento (última fecha con sets)"""
        with get_db() as db:
            query = text("""
                SELECT DATE(s.date) AS dia,
                       COUNT(DISTINCT te.Exercise_idExercise) AS exercises,
                       COUNT(*) AS total_sets
                FROM `Set` s
                JOIN Trainday_exercise te
                  ON s.Trainday_exercise_idTrainday_exercise = te.idTrainday_exercise
                JOIN Trainday td
                  ON te.Trainday_idTrainday = td.idTrainday
                JOIN Trainplan tp
                  ON td.Trainplan_idTrainplan = tp.idTrainplan
                WHERE tp.User_idUser = :user_id
                GROUP BY DATE(s.date)
                ORDER BY dia DESC
                LIMIT 1
            """)
            row = db.execute(query, {"user_id": user_id}).fetchone()

            if row:
                return {
                    "date": str(row[0]),
                    "exercises": int(row[1]),
                    "sets": int(row[2])
                }
            return {"date": None, "exercises": 0, "sets": 0}
