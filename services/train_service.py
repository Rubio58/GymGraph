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
            trainday_exercises = self.repo.get_traindayexercises_by_trainday(db, trainday_id)
            trainday_exercises_list = []
            for tde in trainday_exercises:
                exercise = self.repo.get_exercise_by_id(db, tde.Exercise_idExercise)
                trainday_exercises_list.append({
                    'idTrainday_exercise': tde.idTrainday_exercise,
                    'idTrainday': tde.Trainday_idTrainday,
                    'numSets': tde.numSets,
                    'notes': tde.notes,
                    'order': tde.order,  
                    'exercise_name': exercise.name,
                    'musclegroup': exercise.musclegroup
                })
            # Ordenar la lista por el campo 'order'
            trainday_exercises_list.sort(key=lambda x: x['order'])
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
    
    def get_trainday_by_id(self, trainday_id:int) -> Dict:
        
        with get_db() as db:
            trainday = self.repo.get_trainday_by_id(db,trainday_id)
            trainday_dict={
                'idTrainday': trainday.idTrainday,
                'name': trainday.name,
                'Trainplan_idTrainplan': trainday.Trainplan_idTrainplan
            }
        return trainday_dict     
    
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
    
    def delete_trainday(self, trainday_id: int):
        print(f"SERVICE delete_trainday - ID: {trainday_id}, tipo: {type(trainday_id)}")
        with get_db() as db:
            try:
                # Verificar si existe el trainday
                trainday = self.repo.get_trainday_by_id(db, trainday_id)
                print(f"Trainday encontrado: {trainday}")
                
                if not trainday:
                    return {'success': False, 'error': 'Trainday no encontrado'}
                
                # Obtener ejercicios asociados
                ejercicios = self.repo.get_traindayexercises_by_trainday(db, trainday_id)
                print(f"Ejercicios asociados: {len(ejercicios)}")
                
                for ej in ejercicios:
                    print(f"Eliminando ejercicio: {ej.idTrainday_exercise}")
                    db.delete(ej)
                
                print(f"Eliminando trainday: {trainday_id}")
                self.repo.delete_trainday(db, trainday_id)
                
                db.commit()
                print("COMMIT exitoso")
                return {'success': True}
            except Exception as e:
                db.rollback()
                print(f"ERROR: {str(e)}")
                return {'success': False, 'error': str(e)}
            
    def delete_traindayexercise(self, traindayexercise_id: int):

        with get_db() as db:
            try:                
                
                self.repo.delete_traindayexercise(db, traindayexercise_id)
                
                db.commit()

                return {'success': True}
            except Exception as e:
                db.rollback()
                print(f"ERROR: {str(e)}")
                return {'success': False, 'error': str(e)}            
    
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
                # Obtener el máximo orden actual para este trainday
                ejercicios = self.repo.get_traindayexercises_by_trainday(db, trainday_id)
                max_order = 0
                for ej in ejercicios:
                    if ej.order > max_order:
                        max_order = ej.order
                
                nuevo_orden = max_order + 1
                
                self.repo.create_trainday_exercise(db, numSets, exercise_id, trainday_id, trainplan_id, user_id, notes, nuevo_orden)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
    
    def update_trainday(self, trainday_id:int, new_name:string):
        with get_db() as db:
            try:
                self.repo.update_trainday(db,trainday_id,new_name)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
        return
    
    def update_traindayexercise(self, traindayexercise_id:int, new_notes:string, new_numsets:int):
        with get_db() as db:
            try:
                self.repo.update_traindayexercise(db,traindayexercise_id,new_notes,new_numsets)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
        return    
    
    def update_traindayplan(self, trainplan_id:int, new_name:string):
        with get_db() as db:
            try:
                self.repo.update_trainplan(db,trainplan_id,new_name)
                db.commit()
                return {'success': True}
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
        return   
    
    def move_traindayexercise(self, traindayexercise_id: int, direction: str):
        with get_db() as db:
            try:
                # Obtener el ejercicio actual
                tde_actual = self.repo.get_traindayexercise_by_id(db, traindayexercise_id)
                if not tde_actual:
                    return {'success': False, 'error': 'Ejercicio no encontrado'}
                
                trainday_id = tde_actual.Trainday_idTrainday
                
                # Obtener todos los ejercicios del mismo trainday ordenados
                ejercicios = self.repo.get_traindayexercises_by_trainday(db, trainday_id)
                ejercicios_ordenados = sorted(ejercicios, key=lambda x: x.order)
                
                # Encontrar índices
                indice_actual = -1
                for i, ej in enumerate(ejercicios_ordenados):
                    if ej.idTrainday_exercise == traindayexercise_id:
                        indice_actual = i
                        break
                
                if direction == 'up' and indice_actual > 0:
                    # Intercambiar con el anterior
                    ej_anterior = ejercicios_ordenados[indice_actual - 1]
                    tde_actual.order, ej_anterior.order = ej_anterior.order, tde_actual.order
                    
                elif direction == 'down' and indice_actual < len(ejercicios_ordenados) - 1:
                    # Intercambiar con el siguiente
                    ej_siguiente = ejercicios_ordenados[indice_actual + 1]
                    tde_actual.order, ej_siguiente.order = ej_siguiente.order, tde_actual.order
                
                db.commit()
                return {'success': True}
                
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}    
        