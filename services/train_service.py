# services/train_service.py
import string
from typing import Dict, List
from repositories.train_repository import TrainRepository
from database import get_db

class TrainService:

    def __init__(self):
        self.repo = TrainRepository()

    def get_trainplans(self, user_id:int) -> List[Dict]:
        
        with get_db() as db:
            trainplans=self.repo.get_trainplans_by_user_id(db,user_id)
            trainplan_list=[]
            for tp in trainplans:
                trainplan_list.append({
                    'idTrainplan': tp.idTrainplan,
                    'name': tp.name
                })
        return trainplan_list
    
    def create_trainplan(self, user_id:int, name:string):
        with get_db() as db:
            try:
                self.repo.create_trainplan(db,user_id,name)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
        return
    
    def delete_trainplan(self, trainplan_id:int):
        with get_db() as db:
            try:
                self.repo.delete_trainplan(db,trainplan_id)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
        return
    
    def get_traindays_by_trainplan(self, trainplan_id:int) -> List[Dict]:
        
        with get_db() as db:
            traindays=self.repo.get_traindays_by_trainplan(db,trainplan_id)
            traindays_list=[]
            for td in traindays:
                traindays_list.append({
                    'idTrainday': td.idTrainday,
                    'name': td.name
                })
        return traindays_list
    
    def get_traindayexercises_by_trainday(self, trainday_id:int) -> List[Dict]:
        
        with get_db() as db:
            trainday_exercises=self.repo.get_traindayexercises_by_trainday(db,trainday_id)
            trainday_exercises_list=[]
            for tde in trainday_exercises:
                exercise=self.repo.get_exercise_by_id(db,tde.Exercise_idExercise)
                trainday_exercises_list.append({
                    'idTrainday_exercise': tde.idTrainday_exercise,
                    'idTrainday': tde.Trainday_idTrainday,
                    'numSets': tde.numSets,
                    'notes': tde.notes,
                    'exercise_name': exercise.name,
                    'musclegroup':exercise.musclegroup
                })
        return trainday_exercises_list    
    
    def get_exercise_by_traindayexercise(self, traindayexercise_id:int) -> Dict:
        
        with get_db() as db:
            exercise=self.repo.get_exercise_by_traindayexercise(db,traindayexercise_id)
            exercise_dict={
                'idExercise': exercise.idExercise,
                'name': exercise.name,
                'musclegroup': exercise.musclegroup
            }
        return exercise_dict 
    
    def create_trainday(self, user_id:int, name:string, trainplan_id:int):
        with get_db() as db:
            try:
                self.repo.create_trainday(db, trainplan_id, name, user_id)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
        return
    
    def delete_trainday(self, trainday_id:int):
        with get_db() as db:
            try:
                self.repo.delete_trainday(db,trainday_id)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
        return    
    
    def get_exercises(self):
        with get_db() as db:
            exercises=self.repo.get_all_exercises(db)
            exercises_list=[]
            for ex in exercises:
                exercises_list.append({
                    'idExercise':ex.idExercise,
                    'name': ex.name,
                    'musclegroup': ex.musclegroup
                })
        return exercises_list
    
    def create_trainday_exercise(self, numSets:int, exercise_id:int, trainday_id:int, trainplan_id:int, user_id:int, notes:string=None):
        with get_db() as db:
            try:
                self.repo.create_trainday_exercise(db,numSets, exercise_id,trainday_id,trainplan_id,user_id,notes)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
        return

        