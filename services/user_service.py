# services/user_service.py

import string
from database import get_db
from repositories.user_repository import UserRepository


class UserService:
    
    def __init__(self):
        self.repo = UserRepository()

    def get_objectives_by_user(self, user_id:int):

        with get_db() as db:
            objectives=self.repo.get_or_create_objective(db,user_id)
            exercise_dict={
                'protein': objectives.protein,
                'carbs': objectives.carbs,
                'fats': objectives.fats
            }
            return exercise_dict
        
    def update_objectives(self, user_id: int, protein: int, carbs: int, fats: int):
        """Actualizar los objetivos nutricionales de un usuario"""
        with get_db() as db:
            self.repo.update_objective(db, user_id, protein, carbs, fats)
            db.commit()
            return 

    def update_username(self, user_id:int, username:string ):
        """Actualizar los objetivos nutricionales de un usuario"""
        with get_db() as db:
            self.repo.update_username(db,username,user_id)
            db.commit()
            return        