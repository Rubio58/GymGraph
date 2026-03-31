from database import engine
from sqlalchemy import text

def migrate():
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        
        # Add new columns (ignore if they exist)
        try:
            conn.execute(text("ALTER TABLE `Set` ADD COLUMN `Exercise_idExercise` INT;"))
        except:
            pass
        try:
            conn.execute(text("ALTER TABLE `Set` ADD COLUMN `User_idUser` INT;"))
        except:
            pass
        
        # Populate new columns
        update_query = """
        UPDATE `Set` s
        JOIN `Trainday_exercise` te ON s.Trainday_exercise_idTrainday_exercise = te.idTrainday_exercise
        JOIN `Trainday` td ON te.Trainday_idTrainday = td.idTrainday
        JOIN `Trainplan` tp ON td.Trainplan_idTrainplan = tp.idTrainplan
        SET s.Exercise_idExercise = te.Exercise_idExercise,
            s.User_idUser = tp.User_idUser;
        """
        conn.execute(text(update_query))
        
        # Drop old constraints
        try:
            conn.execute(text("ALTER TABLE `Set` DROP FOREIGN KEY `fk_Set_Trainday_exercise1`;"))
        except:
            pass
        try:
            conn.execute(text("ALTER TABLE `Set` DROP INDEX `fk_Set_Trainday_exercise1_idx`;"))
        except:
            pass
        
        # Update primary key and drop old column
        try:
            conn.execute(text("ALTER TABLE `Set` DROP PRIMARY KEY;"))
        except:
            pass
            
        try:
            conn.execute(text("ALTER TABLE `Set` DROP COLUMN `Trainday_exercise_idTrainday_exercise`;"))
        except:
            pass
        
        # Modify new columns
        conn.execute(text("ALTER TABLE `Set` MODIFY COLUMN `Exercise_idExercise` INT NOT NULL;"))
        conn.execute(text("ALTER TABLE `Set` MODIFY COLUMN `User_idUser` INT NOT NULL;"))
        try:
            conn.execute(text("ALTER TABLE `Set` ADD PRIMARY KEY (`idSet`, `Exercise_idExercise`, `User_idUser`);"))
        except:
            pass
        
        # Add new foreign keys and indexes
        try:
            conn.execute(text("ALTER TABLE `Set` ADD CONSTRAINT `fk_Set_Exercise1` FOREIGN KEY (`Exercise_idExercise`) REFERENCES `Exercise` (`idExercise`) ON DELETE RESTRICT ON UPDATE RESTRICT;"))
        except:
            pass
        try:
            conn.execute(text("ALTER TABLE `Set` ADD CONSTRAINT `fk_Set_User1` FOREIGN KEY (`User_idUser`) REFERENCES `User` (`idUser`) ON DELETE RESTRICT ON UPDATE RESTRICT;"))
        except:
            pass
        try:
            conn.execute(text("ALTER TABLE `Set` ADD INDEX `fk_Set_Exercise1_idx` (`Exercise_idExercise`);"))
        except:
            pass
        try:
            conn.execute(text("ALTER TABLE `Set` ADD INDEX `fk_Set_User1_idx` (`User_idUser`);"))
        except:
            pass
        
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

if __name__ == '__main__':
    try:
        migrate()
        print("Migration successful")
    except Exception as e:
        print("Migration failed:", e)
