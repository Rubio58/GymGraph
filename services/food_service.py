# services/food_service.py
from repositories.food_repository import FoodRepository
from database import get_db
from typing import List, Dict
from datetime import datetime

class FoodService:
    """Lógica de negocio para alimentos y comidas"""
    
    def __init__(self):
        self.repo = FoodRepository()
    
    # ===== FOOD =====
    def get_user_foods(self, user_id: int):
        """Obtiene SOLO los alimentos del usuario especificado"""
        with get_db() as db:
            foods = self.repo.get_food_by_user_id(db, user_id)
            return [
                {
                    'id': f.idFood,
                    'name': f.name,
                    'protein': float(f.protein_p100),
                    'carbs': float(f.carbs_p100),
                    'fats': float(f.fats_p100),
                    'kcal': float(f.kcal_p100) if f.kcal_p100 else 0
                }
                for f in foods
            ]
    
    def create_food(self, user_id:int, name: str, protein: float, carbs: float, fats: float) -> Dict:
        """Crear nuevo alimento"""
        
        with get_db() as db:
            try:
                # 1g proteína = 4 kcal
                # 1g carbohidratos = 4 kcal  
                # 1g grasa = 9 kcal
                kcal = (protein * 4) + (carbs * 4) + (fats * 9)

                food = self.repo.create_food(db, user_id, name, protein, carbs, fats, kcal)

                return {
                    'success': True,
                    'food': {
                        'id': food.idFood,
                        'name': food.name,
                        'protein': float(food.protein_p100),
                        'carbs': float(food.carbs_p100),
                        'fats': float(food.fats_p100),
                        'kcal': float(food.kcal_p100)
                    }
                }
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
    
    # ===== MEAL =====
    def create_meal(self, user_id: int, foods_data: List[Dict]) -> Dict:
        """
        foods_data: [{'food_id': 1, 'grams': 100}, ...]
        """
        with get_db() as db:
            try:
                print(f"FoodService.create_meal: {len(foods_data)} alimentos")  # DEBUG
                
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                meal = self.repo.create_meal(db, user_id, date)
                print(f"Meal creada: {meal.idMeal}")  # DEBUG
                
                for i, item in enumerate(foods_data):
                    print(f"Guardando alimento {i+1}: food_id={item['food_id']}, grams={item['grams']}")  # DEBUG
                    
                    if 'food_id' not in item or 'grams' not in item:
                        return {'success': False, 'error': 'Invalid food data format'}
                    
                    self.repo.create_meal_food(
                        db, 
                        meal.idMeal, 
                        user_id, 
                        item['food_id'], 
                        item['grams']
                    )
                
                return {
                    'success': True,
                    'message': f'Comida creada con {len(foods_data)} alimentos',
                }
                    
            except Exception as e:
                db.rollback()
                print(f"ERROR en create_meal: {str(e)}")  # DEBUG
                return {'success': False, 'error': str(e)}
            
    def delete_meal(self, meal_id:int):
        with get_db() as db:
            try:
                self.repo.delete_meal(db,meal_id)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
            
    def update_meal(self, user_id: int, meal_id: int, foods_data: List[Dict]) -> Dict:
        """
        Actualiza una comida existente
        """
        with get_db() as db:
            try:
                # 1. Verificar que la comida existe
                meal = self.repo.get_meal_by_id(db, meal_id, user_id)
                if not meal:
                    return {'success': False, 'error': 'Comida no encontrada'}
                
                # 2. Eliminar todos los MealFood existentes
                current_meal_foods = self.repo.get_meal_foods_by_meal(db, meal_id)
                for mf in current_meal_foods:
                    db.delete(mf)
                
                # 3. Crear todos los MealFood de nuevo con los datos del formulario
                for item in foods_data:
                    self.repo.create_meal_food(
                        db,
                        meal_id,
                        user_id,
                        item['food_id'],
                        item['grams']
                    )
                
                db.commit()
                
                return {
                    'success': True,
                    'message': 'Comida actualizada correctamente'
                }
                
            except Exception as e:
                db.rollback()
                print(f"ERROR en update_meal: {str(e)}")
                return {'success': False, 'error': str(e)}