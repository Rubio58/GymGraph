# repositories/user_repository.py
from models import Objective, User

class UserRepository:
    """SOLO consultas a la base de datos"""
    
    def get_by_username(self, db, username):
        """Buscar usuario por nombre de usuario"""
        return db.query(User).filter(User.username == username).first()
    
    def get_by_id(self, db, user_id):
        """Buscar usuario por ID"""
        return db.query(User).filter(User.idUser == user_id).first()
    
    def create(self, db, username, hashed_password):
        """Crear nuevo usuario"""
        user = User(
            username=username,
            passwd=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def update_username(self, db, new_username, user_id):

        user=self.get_by_id(db,user_id)
        if self.username_exists(db,new_username):
            return 
        user.username=new_username
        db.add(user)
        db.flush()

        return
    
    def username_exists(self, db, username):
        """Verificar si un username ya existe"""
        return db.query(User).filter(User.username == username).first() is not None
    
    def get_or_create_objective(self, db, user_id):
        """Obtener objetivo o crear uno con valores por defecto"""

        objective = self.get_objective_by_user(db, user_id)
        
        if not objective:
            objective = self.create_objective(db, user_id, protein=0, carbs=0, fats=0)
        
        return objective
    
    def get_objective_by_user(self, db, user_id):
        """Obtener el objetivo nutricional de un usuario"""
        return db.query(Objective).filter(Objective.User_idUser == user_id).first()
    
    def create_objective(self, db, user_id, protein, carbs, fats):
        """Crear un nuevo objetivo nutricional para un usuario"""
        objective = Objective(
            protein=protein,
            carbs=carbs,
            fats=fats,
            User_idUser=user_id
        )
        db.add(objective)
        db.flush()
        return objective
    
    def update_objective(self, db, user_id, protein, carbs, fats):
        """Actualizar el objetivo nutricional de un usuario"""
        objective = db.query(Objective).filter(Objective.User_idUser == user_id).first()
        
        if objective:
            # Actualizar objetivo existente
            objective.protein = protein
            objective.carbs = carbs
            objective.fats = fats
        else:
            # Crear nuevo objetivo si no existe
            objective = Objective(
                protein=protein,
                carbs=carbs,
                fats=fats,
                User_idUser=user_id
            )
            db.add(objective)
        
        db.flush()
        return 