"""
Servicio de análisis avanzado: correlaciones, covarianzas y estadísticas
"""

from database import SessionLocal
from models import User, Food, Meal, MealFood, Exercise, Trainplan, Trainday, TraindayExercise, Set, Meas, MeasCat
from datetime import date, datetime, timedelta
from sqlalchemy import func, text
import math
from decimal import Decimal


class AnalysisService:
    """Servicios de análisis estadístico de datos de fitness"""

    def __init__(self):
        self.session = SessionLocal()

    def get_metric_data(self, user_id, metric_type, days=30, start_date=None, end_date=None, all_time=False):
        """
        Obtiene datos de una métrica a través del tiempo
        Tipos: calories, protein, carbs, fats, weight_avg, volume, sets, reps_avg,
               meals_count, workouts_count, meas_<id>
        """
        if end_date is None:
            end_date = date.today()
        is_hourly = False
        if all_time:
            start_date = self._get_first_data_date(user_id)
        elif start_date is None:
            if days == 1:
                start_date = end_date
                is_hourly = True
            else:
                start_date = end_date - timedelta(days=days - 1)
        elif start_date == end_date:
            is_hourly = True

        if metric_type == 'calories':
            return self._get_calories_data(user_id, start_date, end_date, is_hourly)
        elif metric_type == 'protein':
            return self._get_macros_data(user_id, start_date, end_date, 'protein', is_hourly)
        elif metric_type == 'carbs':
            return self._get_macros_data(user_id, start_date, end_date, 'carbs', is_hourly)
        elif metric_type == 'fats':
            return self._get_macros_data(user_id, start_date, end_date, 'fats', is_hourly)
        elif metric_type == 'weight_avg':
            return self._get_weight_avg_data(user_id, start_date, end_date, is_hourly)
        elif metric_type == 'volume':
            return self._get_volume_data(user_id, start_date, end_date, is_hourly)
        elif metric_type == 'sets':
            return self._get_sets_data(user_id, start_date, end_date, is_hourly)
        elif metric_type == 'reps_avg':
            return self._get_reps_avg_data(user_id, start_date, end_date, is_hourly)
        elif metric_type == 'meals_count':
            return self._get_meals_count_data(user_id, start_date, end_date, is_hourly)
        elif metric_type == 'workouts_count':
            return self._get_workouts_count_data(user_id, start_date, end_date, is_hourly)
        elif metric_type.startswith('meas_'):
            cat_id = int(metric_type.split('_', 1)[1])
            return self._get_meas_data(user_id, cat_id, start_date, end_date, is_hourly)
        else:
            return {'labels': [], 'data': []}

    def _get_grouping_col(self, col, is_hourly):
        if is_hourly:
            return func.date_format(col, '%H:00')
        return func.date(col)

    def _get_calories_data(self, user_id, start_date, end_date, is_hourly):
        """Calorías consumidas por día o por hora"""
        group_col = self._get_grouping_col(Meal.date, is_hourly)
        result = self.session.query(
            group_col.label('date_label'),
            func.sum((MealFood.grams * Food.kcal_p100) / 100).label('kcal')
        ).join(
            MealFood, Meal.idMeal == MealFood.Meal_idMeal
        ).join(
            Food, MealFood.Food_idFood == Food.idFood
        ).filter(
            Meal.User_idUser == user_id,
            func.date(Meal.date) >= start_date,
            func.date(Meal.date) <= end_date
        ).group_by(
            group_col
        ).order_by(
            group_col
        ).all()

        return self._format_result(result, is_hourly, 'kcal', start_date)

    def _get_macros_data(self, user_id, start_date, end_date, macro_type, is_hourly):
        """Macros por día o por hora (protein, carbs, fats)"""
        group_col = self._get_grouping_col(Meal.date, is_hourly)
        result = self.session.query(
            group_col.label('date_label'),
            func.sum((MealFood.grams * getattr(Food, f'{macro_type}_p100')) / 100).label('amount')
        ).join(
            MealFood, Meal.idMeal == MealFood.Meal_idMeal
        ).join(
            Food, MealFood.Food_idFood == Food.idFood
        ).filter(
            Meal.User_idUser == user_id,
            func.date(Meal.date) >= start_date,
            func.date(Meal.date) <= end_date
        ).group_by(
            group_col
        ).order_by(
            group_col
        ).all()

        return self._format_result(result, is_hourly, 'amount', start_date)

    def _get_weight_avg_data(self, user_id, start_date, end_date, is_hourly):
        """Promedio de peso levantado por día o por hora"""
        group_col = self._get_grouping_col(Set.date, is_hourly)
        result = self.session.query(
            group_col.label('date_label'),
            func.avg(Set.weight).label('avg_weight')
        ).filter(
            Set.User_idUser == user_id,
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            group_col
        ).order_by(
            group_col
        ).all()

        return self._format_result(result, is_hourly, 'avg_weight', start_date)

    def _get_volume_data(self, user_id, start_date, end_date, is_hourly):
        """Volumen total de entrenamiento por día o por hora"""
        group_col = self._get_grouping_col(Set.date, is_hourly)
        result = self.session.query(
            group_col.label('date_label'),
            func.sum(Set.weight * Set.reps).label('total_volume')
        ).filter(
            Set.User_idUser == user_id,
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            group_col
        ).order_by(
            group_col
        ).all()

        return self._format_result(result, is_hourly, 'total_volume', start_date)

    def _get_sets_data(self, user_id, start_date, end_date, is_hourly):
        """Total de series por día o por hora"""
        group_col = self._get_grouping_col(Set.date, is_hourly)
        result = self.session.query(
            group_col.label('date_label'),
            func.count(Set.idSet).label('total_sets')
        ).filter(
            Set.User_idUser == user_id,
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            group_col
        ).order_by(
            group_col
        ).all()

        return self._format_result(result, is_hourly, 'total_sets', start_date)

    def _get_reps_avg_data(self, user_id, start_date, end_date, is_hourly):
        """Promedio de reps por día o por hora"""
        group_col = self._get_grouping_col(Set.date, is_hourly)
        result = self.session.query(
            group_col.label('date_label'),
            func.avg(Set.reps).label('avg_reps')
        ).filter(
            Set.User_idUser == user_id,
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            group_col
        ).order_by(
            group_col
        ).all()

        return self._format_result(result, is_hourly, 'avg_reps', start_date)

    def _get_meals_count_data(self, user_id, start_date, end_date, is_hourly):
        """Número de comidas por día o por hora"""
        group_col = self._get_grouping_col(Meal.date, is_hourly)
        result = self.session.query(
            group_col.label('date_label'),
            func.count(Meal.idMeal).label('meal_count')
        ).filter(
            Meal.User_idUser == user_id,
            func.date(Meal.date) >= start_date,
            func.date(Meal.date) <= end_date
        ).group_by(
            group_col
        ).order_by(
            group_col
        ).all()

        return self._format_result(result, is_hourly, 'meal_count', start_date)

    def _get_workouts_count_data(self, user_id, start_date, end_date, is_hourly):
        """Número de entrenamientos por día o por hora"""
        group_col = self._get_grouping_col(Set.date, is_hourly)
        result = self.session.query(
            group_col.label('date_label'),
            func.count(func.distinct(func.date(Set.date))).label('workout_count')
        ).filter(
            Set.User_idUser == user_id,
            func.date(Set.date) >= start_date,
            func.date(Set.date) <= end_date
        ).group_by(
            group_col
        ).order_by(
            group_col
        ).all()

        return self._format_result(result, is_hourly, 'workout_count', start_date)

    def _get_first_data_date(self, user_id):
        """Retorna la fecha del primer dato registrado por el usuario en cualquier tabla"""
        candidates = []
        meal_min = self.session.query(func.min(Meal.date)).filter(Meal.User_idUser == user_id).scalar()
        if meal_min:
            candidates.append(date.fromisoformat(str(meal_min)[:10]))
        set_min = self.session.query(func.min(func.date(Set.date))).filter(
            Set.User_idUser == user_id
        ).scalar()
        if set_min:
            candidates.append(set_min if isinstance(set_min, date) else date.fromisoformat(str(set_min)[:10]))
        meas_min = self.session.query(func.min(Meas.date)).filter(Meas.User_idUser == user_id).scalar()
        if meas_min:
            candidates.append(date.fromisoformat(str(meas_min)[:10]))
        return min(candidates) if candidates else date.today() - timedelta(days=30)

    def _get_meas_data(self, user_id, meas_cat_id, start_date, end_date, is_hourly):
        """Medidas corporales de una categoría concreta"""
        group_col = self._get_grouping_col(Meas.date, is_hourly)
        result = self.session.query(
            group_col.label('date_label'),
            Meas.val.label('val')
        ).filter(
            Meas.User_idUser == user_id,
            Meas.MeasCat_idMeasCat == meas_cat_id,
            func.date(Meas.date) >= start_date,
            func.date(Meas.date) <= end_date
        ).order_by(group_col).all()

        # Medidas no se agrupan promediando en SQL para mantener simplicidad,
        # pero para graficar por hora sí se debería promediar o rellenar
        # Lo manejaremos usando _format_result también si la db no explotó
        return self._format_result(result, is_hourly, 'val', start_date)

    def _format_result(self, result_rows, is_hourly, val_col, start_date):
        """Aplica relleno de horas si es horario, o formatea a listas regulares"""
        data_dict = {}
        for r in result_rows:
            key = str(r.date_label)
            val = getattr(r, val_col)
            if val is not None:
                data_dict[key] = float(val)

        if not is_hourly:
            # Result normal
            return {
                'labels': sorted(data_dict.keys()),
                'data': [data_dict[k] for k in sorted(data_dict.keys())]
            }

        # Rellenar 00:00 a 23:00 para la fecha start_date
        labels = []
        data = []
        for i in range(24):
            hour_str = f"{i:02d}:00"
            labels.append(hour_str)
            data.append(data_dict.get(hour_str, 0.0))
            
        return {'labels': labels, 'data': data}

    def calculate_correlation(self, user_id, metric1, metric2, days=30, start_date=None, end_date=None, all_time=False):
        """Calcula la correlación de Pearson entre dos métricas"""
        data1 = self.get_metric_data(user_id, metric1, days, start_date=start_date, end_date=end_date, all_time=all_time)
        data2 = self.get_metric_data(user_id, metric2, days, start_date=start_date, end_date=end_date, all_time=all_time)

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
            strength = "very strong"
        elif abs_r >= 0.7:
            strength = "strong"
        elif abs_r >= 0.5:
            strength = "moderate"
        elif abs_r >= 0.3:
            strength = "weak"
        else:
            strength = "very weak or non-existent"

        if r > 0:
            direction = "positive"
            explanation = "When one increases, the other tends to increase"
        elif r < 0:
            direction = "negative"
            explanation = "When one increases, the other tends to decrease"
        else:
            direction = "none"
            explanation = "No linear relationship apparent"

        return {
            'strength': strength,
            'direction': direction,
            'explanation': explanation,
            'r_value': r
        }

    def get_available_metrics(self, user_id=None):
        """Retorna la lista de métricas disponibles. Si se pasa user_id incluye medidas corporales del usuario."""
        metrics = [
            {'id': 'calories', 'name': 'Calories', 'category': 'Nutrition', 'unit': 'kcal'},
            {'id': 'protein', 'name': 'Protein', 'category': 'Nutrition', 'unit': 'g'},
            {'id': 'carbs', 'name': 'Carbs', 'category': 'Nutrition', 'unit': 'g'},
            {'id': 'fats', 'name': 'Fats', 'category': 'Nutrition', 'unit': 'g'},
            {'id': 'weight_avg', 'name': 'Avg Weight Lifted', 'category': 'Training', 'unit': 'kg'},
            {'id': 'volume', 'name': 'Total Volume', 'category': 'Training', 'unit': 'kg'},
        ]
        if user_id:
            cats = self.session.query(MeasCat).join(
                Meas, MeasCat.idMeasCat == Meas.MeasCat_idMeasCat
            ).filter(Meas.User_idUser == user_id).distinct().order_by(MeasCat.name).all()
            for cat in cats:
                metrics.append({
                    'id': f'meas_{cat.idMeasCat}',
                    'name': cat.name,
                    'category': 'Measurements',
                    'unit': cat.unit
                })
        return metrics

    def close(self):
        """Cierra la sesión"""
        self.session.close()
