"""
Servicio de análisis avanzado: correlaciones, covarianzas y estadísticas
"""

from database import SessionLocal
from models import User, Food, Meal, MealFood, Exercise, Trainplan, Trainday, TraindayExercise, Set
from datetime import date, datetime, timedelta
from sqlalchemy import func, text
import math
from decimal import Decimal


class AnalysisService:
    """Servicios de análisis estadístico de datos de fitness"""

    def __init__(self):
        self.session = SessionLocal()

    def get_metric_data(self, user_id, metric_type, days=30):
        """
        Obtiene datos de una métrica a través del tiempo
        Tipos: calories, protein, carbs, fats, weight_per_exercise, volume, sets
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        if metric_type == 'calories':
            return self._get_calories_data(user_id, start_date, end_date)
        elif metric_type == 'protein':
            return self._get_macros_data(user_id, start_date, end_date, 'protein')
        elif metric_type == 'carbs':
            return self._get_macros_data(user_id, start_date, end_date, 'carbs')
        elif metric_type == 'fats':
            return self._get_macros_data(user_id, start_date, end_date, 'fats')
        elif metric_type == 'weight_avg':
            return self._get_weight_avg_data(user_id, start_date, end_date)
        elif metric_type == 'volume':
            return self._get_volume_data(user_id, start_date, end_date)
        elif metric_type == 'sets':
            return self._get_sets_data(user_id, start_date, end_date)
        elif metric_type == 'reps_avg':
            return self._get_reps_avg_data(user_id, start_date, end_date)
        elif metric_type == 'meals_count':
            return self._get_meals_count_data(user_id, start_date, end_date)
        elif metric_type == 'workouts_count':
            return self._get_workouts_count_data(user_id, start_date, end_date)
        else:
            return {'labels': [], 'data': []}

    def _get_calories_data(self, user_id, start_date, end_date):
        """Calorías consumidas por día"""
        result = self.session.query(
            Meal.date.label('date'),
            func.sum((MealFood.grams * Food.kcal_p100) / 100).label('kcal')
        ).join(
            MealFood, Meal.idMeal == MealFood.Meal_idMeal
        ).join(
            Food, MealFood.Food_idFood == Food.idFood
        ).filter(
            Meal.User_idUser == user_id,
            Meal.date >= str(start_date),
            Meal.date <= str(end_date)
        ).group_by(
            Meal.date
        ).order_by(
            Meal.date
        ).all()

        return {
            'labels': [str(r.date) for r in result],
            'data': [float(r.kcal or 0) for r in result]
        }

    def _get_macros_data(self, user_id, start_date, end_date, macro_type):
        """Macros por día (protein, carbs, fats)"""
        result = self.session.query(
            Meal.date.label('date'),
            func.sum((MealFood.grams * getattr(Food, f'{macro_type}_p100')) / 100).label('amount')
        ).join(
            MealFood, Meal.idMeal == MealFood.Meal_idMeal
        ).join(
            Food, MealFood.Food_idFood == Food.idFood
        ).filter(
            Meal.User_idUser == user_id,
            Meal.date >= str(start_date),
            Meal.date <= str(end_date)
        ).group_by(
            Meal.date
        ).order_by(
            Meal.date
        ).all()

        return {
            'labels': [str(r.date) for r in result],
            'data': [float(r.amount or 0) for r in result]
        }

    def _get_weight_avg_data(self, user_id, start_date, end_date):
        """Promedio de peso levantado por día"""
        result = self.session.query(
            func.date(Set.date).label('workout_date'),
            func.avg(Set.weight).label('avg_weight')
        ).join(
            TraindayExercise, Set.Trainday_exercise_idTrainday_exercise == TraindayExercise.idTrainday_exercise
        ).join(
            Trainday, TraindayExercise.Trainday_idTrainday == Trainday.idTrainday
        ).join(
            Trainplan, Trainday.Trainplan_idTrainplan == Trainplan.idTrainplan
        ).filter(
            Trainplan.User_idUser == user_id,
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            func.date(Set.date)
        ).order_by(
            func.date(Set.date)
        ).all()

        return {
            'labels': [str(r.workout_date) for r in result],
            'data': [float(r.avg_weight or 0) for r in result]
        }

    def _get_volume_data(self, user_id, start_date, end_date):
        """Volumen total de entrenamiento por día"""
        result = self.session.query(
            func.date(Set.date).label('workout_date'),
            func.sum(Set.weight * Set.reps).label('total_volume')
        ).join(
            TraindayExercise, Set.Trainday_exercise_idTrainday_exercise == TraindayExercise.idTrainday_exercise
        ).join(
            Trainday, TraindayExercise.Trainday_idTrainday == Trainday.idTrainday
        ).join(
            Trainplan, Trainday.Trainplan_idTrainplan == Trainplan.idTrainplan
        ).filter(
            Trainplan.User_idUser == user_id,
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            func.date(Set.date)
        ).order_by(
            func.date(Set.date)
        ).all()

        return {
            'labels': [str(r.workout_date) for r in result],
            'data': [float(r.total_volume or 0) for r in result]
        }

    def _get_sets_data(self, user_id, start_date, end_date):
        """Total de series por día"""
        result = self.session.query(
            func.date(Set.date).label('workout_date'),
            func.count(Set.idSet).label('total_sets')
        ).join(
            TraindayExercise, Set.Trainday_exercise_idTrainday_exercise == TraindayExercise.idTrainday_exercise
        ).join(
            Trainday, TraindayExercise.Trainday_idTrainday == Trainday.idTrainday
        ).join(
            Trainplan, Trainday.Trainplan_idTrainplan == Trainplan.idTrainplan
        ).filter(
            Trainplan.User_idUser == user_id,
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            func.date(Set.date)
        ).order_by(
            func.date(Set.date)
        ).all()

        return {
            'labels': [str(r.workout_date) for r in result],
            'data': [int(r.total_sets or 0) for r in result]
        }

    def _get_reps_avg_data(self, user_id, start_date, end_date):
        """Promedio de reps por día"""
        result = self.session.query(
            func.date(Set.date).label('workout_date'),
            func.avg(Set.reps).label('avg_reps')
        ).join(
            TraindayExercise, Set.Trainday_exercise_idTrainday_exercise == TraindayExercise.idTrainday_exercise
        ).join(
            Trainday, TraindayExercise.Trainday_idTrainday == Trainday.idTrainday
        ).join(
            Trainplan, Trainday.Trainplan_idTrainplan == Trainplan.idTrainplan
        ).filter(
            Trainplan.User_idUser == user_id,
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            func.date(Set.date)
        ).order_by(
            func.date(Set.date)
        ).all()

        return {
            'labels': [str(r.workout_date) for r in result],
            'data': [float(r.avg_reps or 0) for r in result]
        }

    def _get_meals_count_data(self, user_id, start_date, end_date):
        """Número de comidas por día"""
        result = self.session.query(
            Meal.date.label('date'),
            func.count(Meal.idMeal).label('meal_count')
        ).filter(
            Meal.User_idUser == user_id,
            Meal.date >= str(start_date),
            Meal.date <= str(end_date)
        ).group_by(
            Meal.date
        ).order_by(
            Meal.date
        ).all()

        return {
            'labels': [str(r.date) for r in result],
            'data': [int(r.meal_count or 0) for r in result]
        }

    def _get_workouts_count_data(self, user_id, start_date, end_date):
        """Número de entrenamientos por día"""
        result = self.session.query(
            func.date(Set.date).label('workout_date'),
            func.count(func.distinct(TraindayExercise.Trainday_idTrainday)).label('workout_count')
        ).join(
            TraindayExercise, Set.Trainday_exercise_idTrainday_exercise == TraindayExercise.idTrainday_exercise
        ).filter(
            TraindayExercise.Trainday_idTrainday.in_(
                self.session.query(Trainday.idTrainday).join(
                    Trainplan, Trainday.Trainplan_idTrainplan == Trainplan.idTrainplan
                ).filter(Trainplan.User_idUser == user_id)
            ),
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            func.date(Set.date)
        ).order_by(
            func.date(Set.date)
        ).all()

        return {
            'labels': [str(r.workout_date) for r in result],
            'data': [int(r.workout_count or 0) for r in result]
        }

    def calculate_correlation(self, user_id, metric1, metric2, days=30):
        """Calcula la correlación de Pearson entre dos métricas"""
        data1 = self.get_metric_data(user_id, metric1, days)
        data2 = self.get_metric_data(user_id, metric2, days)

        # Encontrar fechas comunes
        dates1 = set(data1['labels'])
        dates2 = set(data2['labels'])
        common_dates = sorted(list(dates1 & dates2))

        if len(common_dates) < 3:
            return {
                'correlation': None,
                'interpretation': 'No hay suficientes datos coincidentes (mínimo 3 puntos)',
                'common_points': len(common_dates)
            }

        # Mapear datos
        dict1 = dict(zip(data1['labels'], data1['data']))
        dict2 = dict(zip(data2['labels'], data2['data']))

        values1 = [dict1[d] for d in common_dates]
        values2 = [dict2[d] for d in common_dates]

        # Calcular correlación
        correlation = self._pearson_correlation(values1, values2)

        return {
            'correlation': round(correlation, 4),
            'interpretation': self._interpret_correlation(correlation),
            'common_points': len(common_dates),
            'scatter_data': [
                {'x': v1, 'y': v2, 'date': d}
                for d, v1, v2 in zip(common_dates, values1, values2)
            ]
        }

    @staticmethod
    def _pearson_correlation(x, y):
        """Calcula el coeficiente de correlación de Pearson"""
        n = len(x)
        if n == 0:
            return 0

        mean_x = sum(x) / n
        mean_y = sum(y) / n

        dev_x = [xi - mean_x for xi in x]
        dev_y = [yi - mean_y for yi in y]

        sum_dev_xy = sum(dx * dy for dx, dy in zip(dev_x, dev_y))
        sum_dev_x2 = sum(dx ** 2 for dx in dev_x)
        sum_dev_y2 = sum(dy ** 2 for dy in dev_y)

        denominator = math.sqrt(sum_dev_x2 * sum_dev_y2)

        if denominator == 0:
            return 0

        return sum_dev_xy / denominator

    @staticmethod
    def _interpret_correlation(r):
        """Interpreta el coeficiente de correlación"""
        abs_r = abs(r)

        if abs_r >= 0.9:
            strength = "muy fuerte"
        elif abs_r >= 0.7:
            strength = "fuerte"
        elif abs_r >= 0.5:
            strength = "moderada"
        elif abs_r >= 0.3:
            strength = "débil"
        else:
            strength = "muy débil o inexistente"

        if r > 0:
            direction = "positiva"
            explanation = "Cuando una aumenta, la otra tiende a aumentar"
        elif r < 0:
            direction = "negativa"
            explanation = "Cuando una aumenta, la otra tiende a disminuir"
        else:
            direction = "nula"
            explanation = "No hay relación lineal aparente"

        return {
            'strength': strength,
            'direction': direction,
            'explanation': explanation,
            'r_value': r
        }

    def get_available_metrics(self):
        """Retorna la lista de métricas disponibles"""
        return [
            {'id': 'calories', 'name': 'Calorías', 'category': 'Nutrición', 'unit': 'kcal'},
            {'id': 'protein', 'name': 'Proteína', 'category': 'Nutrición', 'unit': 'g'},
            {'id': 'carbs', 'name': 'Carbohidratos', 'category': 'Nutrición', 'unit': 'g'},
            {'id': 'fats', 'name': 'Grasas', 'category': 'Nutrición', 'unit': 'g'},
            {'id': 'weight_avg', 'name': 'Peso promedio levantado', 'category': 'Entrenamiento', 'unit': 'kg'},
            {'id': 'volume', 'name': 'Volumen total', 'category': 'Entrenamiento', 'unit': 'kg'},
            {'id': 'sets', 'name': 'Series totales', 'category': 'Entrenamiento', 'unit': 'series'},
            {'id': 'reps_avg', 'name': 'Reps promedio', 'category': 'Entrenamiento', 'unit': 'reps'},
            {'id': 'meals_count', 'name': 'Nº de comidas', 'category': 'Nutrición', 'unit': 'comidas'},
            {'id': 'workouts_count', 'name': 'Nº de entrenamientos', 'category': 'Entrenamiento', 'unit': 'entrenamientos'},
        ]

    def close(self):
        """Cierra la sesión"""
        self.session.close()
