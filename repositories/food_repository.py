# repositories/food_repository.py
from datetime import datetime
from models import Food, Meal, MealFood
from sqlalchemy.orm import Session
from typing import List, Optional

class FoodRepository:
    """Acceso a BD para alimentos y comidas"""
    
    # ===== FOOD =====
    def get_all_foods(self, db: Session) -> List[Food]:
        """Obtener todos los alimentos"""
        return db.query(Food).all()
    
    def get_food_by_user_id(self, db: Session, user_id: int):
        """Obtiene SOLO los alimentos de un usuario específico"""
        return db.query(Food).filter(Food.User_idUser == user_id).all()
    
    def get_food_by_id(self, db: Session, food_id: int) -> Optional[Food]:
        """Obtener alimento por ID"""
        return db.query(Food).filter(Food.idFood == food_id).first()
    
    def create_food(self, db: Session, user_id: int, name: str, protein: float, carbs: float, fats: float, kcal: float) -> Food:
        """Crear nuevo alimento"""
        food = Food(
            name=name,
            protein_p100=protein,
            carbs_p100=carbs,  
            fats_p100=fats,   
            User_idUser=user_id,  
            kcal_p100=kcal 
        )
        db.add(food)
        db.flush()
        return food
    
    # ===== MEAL =====

    def get_meal_by_id(self, db: Session, meal_id: int, user_id: int):
        """Obtiene una comida específica verificando que pertenezca al usuario"""
        return db.query(Meal).filter(
            Meal.idMeal == meal_id,
            Meal.User_idUser == user_id
        ).first()    

    def get_meals_by_date(self, db: Session, user_id: int, date: datetime) -> List[Meal]:
        """
        Obtiene todas las comidas de un usuario en una fecha específica
        date: objeto datetime (solo se usa la parte de fecha)
        """
        # Crear strings para el inicio y fin del día
        start_date = date.strftime('%Y-%m-%d 00:00:00')
        end_date = date.strftime('%Y-%m-%d 23:59:59')
        
        return db.query(Meal).filter(
            Meal.User_idUser == user_id,
            Meal.date >= start_date,
            Meal.date <= end_date
        ).all()
    
    def get_meal_foods_by_meal(self, db:Session, meal_id:int):
        return db.query(MealFood).filter(MealFood.Meal_idMeal == meal_id).all()

    def create_meal(self, db: Session, user_id: int, date: str) -> Meal:
        """Crear nueva comida"""
        meal = Meal(
            date=date,
            User_idUser=user_id
        )
        db.add(meal)
        db.flush()  # Envía a BD pero no hace commit
        return meal
    
    def create_meal_food(self, db: Session, meal_id: int, user_id: int, food_id: int, grams: float):
        """Añade un alimento a una comida"""
        meal_food = MealFood(
            grams=grams,
            Food_idFood=food_id,
            Meal_idMeal=meal_id
        )
        db.add(meal_food)
        db.flush()  # Envía a BD pero no hace commit
        return meal_food  
    
    def delete_meal_food(self, db: Session, meal_food_id: int):
        """Elimina un alimento de una comida"""
        meal_food = db.query(MealFood).filter(MealFood.idMeal_Food == meal_food_id).first()
        if meal_food:
            db.delete(meal_food)
            return True
        return False
    
    def delete_meal(self, db:Session, meal_id: int):
        "Elimina meal y meal_foods asociados"
        meal=db.query(Meal).filter(Meal.idMeal == meal_id).first()
        meal_foods=db.query(MealFood).filter(MealFood.Meal_idMeal == meal_id).all()

        for mf in meal_foods:
            db.delete(mf)

        db.delete(meal)
        return
