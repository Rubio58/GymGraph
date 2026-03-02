# repositories/train_repository.py
import string
from models import Trainday, Trainplan, TraindayExercise, Exercise
from sqlalchemy.orm import Session

class TrainRepository:

    def get_trainplans_by_user_id(self, db: Session, user_id: int):
        return db.query(Trainplan).filter(Trainplan.User_idUser == user_id)
    
    def create_trainplan(self, db: Session, user_id:int, name: string):

        trainplan=Trainplan(
            name=name,
            User_idUser=user_id
        )

        db.add(trainplan)
        db.flush()
        return
    
    def delete_trainplan(self, db:Session, trainplan_id:int):

        trainplan=db.query(Trainplan).filter(Trainplan.idTrainplan == trainplan_id).first()
        traindays=db.query(Trainday).filter(Trainday.Trainplan_idTrainplan == trainplan_id).all()
        for td in traindays:
            traindayexercises=db.query(TraindayExercise).filter(TraindayExercise.Trainday_idTrainday == td.idTrainday).all()
            for tde in traindayexercises:
                db.delete(tde)
            db.delete(td)    
        db.delete(trainplan)
        return
    
    def get_traindays_by_trainplan(self, db: Session, trainplan_id:int):
        return db.query(Trainday).filter(Trainday.Trainplan_idTrainplan == trainplan_id).all()
    
    def get_traindayexercises_by_trainday(self, db:Session, trainday_id:int):
        return db.query(TraindayExercise).filter(TraindayExercise.Trainday_idTrainday == trainday_id).all()
    
    def get_exercise_by_traindayexercise(self, db:Session, traindayexercise_id:int):

        traindayexercise=db.query(TraindayExercise).filter(TraindayExercise.idTrainday_exercise == traindayexercise_id).first()
        return db.query(Exercise).filter(Exercise.idExercise == traindayexercise.Exercise_idExercise).first()

    def create_trainday(self, db: Session, trainplan_id:int, name:string, user_id:int):
        trainday=Trainday(
            name=name,
            Trainplan_idTrainplan=trainplan_id,
            Trainplan_User_idUser=user_id
        )
        db.add(trainday)
        db.flush()
        return    

    def delete_trainday(self, db:Session, trainday_id:int):
        td = db.query(Trainday).filter(Trainday.idTrainday == trainday_id)
        db.delete(td)
        return    
    
    def get_all_exercises(self, db:Session):
        return db.query(Exercise).all()
    
    def create_trainday_exercise(self, db:Session, numSets:int, exercise_id:int, trainday_id:int, trainplan_id:int, user_id:int, notes:string):
        traindayexercise=TraindayExercise(
            numSets=numSets,
            Exercise_idExercise=exercise_id,
            Trainday_idTrainday=trainday_id,
            Trainday_Trainplan_idTrainplan=trainplan_id,
            Trainday_Trainplan_User_idUser=user_id,
            notes=notes
        )
        db.add(traindayexercise)
        db.flush()
        return
    
    def get_exercise_by_id(self, db:Session, exercise_id:int):
        return db.query(Exercise).filter(Exercise.idExercise == exercise_id).first()