# services/macros_service.py
from repositories.food_repository import FoodRepository
from database import get_db
from datetime import datetime
from typing import List, Dict

class MacrosService:
    """Lógica de negocio para la página de macros"""
    
    def __init__(self):
        self.repo = FoodRepository()
    
    def get_meals_by_date(self, user_id: int, date: datetime) -> List[Dict]:
        """
        Obtiene todas las comidas de un usuario en una fecha específica
        date: objeto datetime
        """
        with get_db() as db:
            # Usar el método del repositorio directamente
            meals = self.repo.get_meals_by_date(db, user_id, date)
            
            # 2. Para cada comida, obtener sus alimentos
            meals_list = []
            for meal in meals:
                meal_foods = self.repo.get_meal_foods_by_meal(db, meal.idMeal)
                
                foods_list = []
                totals = {'protein': 0.0, 'carbs': 0.0, 'fats': 0.0, 'kcal': 0.0}
                
                for mf in meal_foods:
                    # Obtener el alimento
                    food = self.repo.get_food_by_id(db, mf.Food_idFood)
                    
                    if food:
                        grams = float(mf.grams)
                        protein_p100 = float(food.protein_p100)
                        carbs_p100 = float(food.carbs_p100)
                        fats_p100 = float(food.fats_p100)
                        kcal_p100 = float(food.kcal_p100) if food.kcal_p100 else 0
                        
                        # Calcular macros según gramos consumidos
                        protein = protein_p100 * grams / 100
                        carbs = carbs_p100 * grams / 100
                        fats = fats_p100 * grams / 100
                        kcal = kcal_p100 * grams / 100
                        
                        foods_list.append({
                            'name': food.name,
                            'grams': grams,
                            'protein': protein,
                            'carbs': carbs,
                            'fats': fats,
                            'kcal': kcal,
                            'food_id': food.idFood,
                            'meal_food_id': mf.idMeal_Food
                        })
                        
                        # Acumular totales
                        totals['protein'] += protein
                        totals['carbs'] += carbs
                        totals['fats'] += fats
                        totals['kcal'] += kcal
                
                meals_list.append({
                    'id': meal.idMeal,
                    'date': meal.date,
                    'foods': foods_list,
                    'totals': totals
                })
            
            return meals_list
    
    def get_daily_totals(self, user_id: int, date: datetime) -> Dict:
        """
        Calcula los totales del día sumando todas las comidas
        """
        meals = self.get_meals_by_date(user_id, date)
        
        totals = {'protein': 0.0, 'carbs': 0.0, 'fats': 0.0, 'kcal': 0.0}
        
        for meal in meals:
            totals['protein'] += meal['totals']['protein']
            totals['carbs'] += meal['totals']['carbs']
            totals['fats'] += meal['totals']['fats']
            totals['kcal'] += meal['totals']['kcal']
        
        return totals

