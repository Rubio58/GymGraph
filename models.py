from typing import Optional
import datetime
import decimal

from sqlalchemy import DECIMAL, DateTime, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Exercise(Base):
    __tablename__ = 'Exercise'
    __table_args__ = (
        Index('idExercise_UNIQUE', 'idExercise', unique=True),
    )

    idExercise: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    musclegroup: Mapped[str] = mapped_column(String(45), nullable=False)

    Trainday_exercise: Mapped[list['TraindayExercise']] = relationship('TraindayExercise', back_populates='Exercise_')


class User(Base):
    __tablename__ = 'User'
    __table_args__ = (
        Index('idUser_UNIQUE', 'idUser', unique=True),
        Index('username_UNIQUE', 'username', unique=True)
    )

    idUser: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(45), nullable=False)
    passwd: Mapped[str] = mapped_column(String(255), nullable=False)

    Food: Mapped[list['Food']] = relationship('Food', back_populates='User_')
    Meal: Mapped[list['Meal']] = relationship('Meal', back_populates='User_')
    Objective: Mapped[list['Objective']] = relationship('Objective', back_populates='User_')
    Trainplan: Mapped[list['Trainplan']] = relationship('Trainplan', back_populates='User_')


class Food(Base):
    __tablename__ = 'Food'
    __table_args__ = (
        ForeignKeyConstraint(['User_idUser'], ['User.idUser'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Food_User1'),
        Index('fk_Food_User1_idx', 'User_idUser'),
        Index('idFood_UNIQUE', 'idFood', unique=True)
    )

    idFood: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    protein_p100: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    carbs_p100: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    fats_p100: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    User_idUser: Mapped[int] = mapped_column(Integer, primary_key=True)
    kcal_p100: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(5, 2))

    User_: Mapped['User'] = relationship('User', back_populates='Food')
    Meal_Food: Mapped[list['MealFood']] = relationship('MealFood', back_populates='Food_')


class Meal(Base):
    __tablename__ = 'Meal'
    __table_args__ = (
        ForeignKeyConstraint(['User_idUser'], ['User.idUser'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Meal_User1'),
        Index('fk_Meal_User1_idx', 'User_idUser'),
        Index('idMeal_UNIQUE', 'idMeal', unique=True)
    )

    idMeal: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(String(45), nullable=False)
    User_idUser: Mapped[int] = mapped_column(Integer, primary_key=True)

    User_: Mapped['User'] = relationship('User', back_populates='Meal')
    Meal_Food: Mapped[list['MealFood']] = relationship('MealFood', back_populates='Meal_')


class Objective(Base):
    __tablename__ = 'Objective'
    __table_args__ = (
        ForeignKeyConstraint(['User_idUser'], ['User.idUser'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Objective_User1'),
        Index('fk_Objective_User1_idx', 'User_idUser'),
        Index('idObjective_UNIQUE', 'idObjective', unique=True)
    )

    idObjective: Mapped[int] = mapped_column(Integer, primary_key=True)
    Protein: Mapped[int] = mapped_column(Integer, nullable=False)
    Carbs: Mapped[int] = mapped_column(Integer, nullable=False)
    Fats: Mapped[int] = mapped_column(Integer, nullable=False)
    User_idUser: Mapped[int] = mapped_column(Integer, primary_key=True)

    User_: Mapped['User'] = relationship('User', back_populates='Objective')


class Trainplan(Base):
    __tablename__ = 'Trainplan'
    __table_args__ = (
        ForeignKeyConstraint(['User_idUser'], ['User.idUser'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Trainplan_User'),
        Index('fk_Trainplan_User_idx', 'User_idUser'),
        Index('idTrainplan_UNIQUE', 'idTrainplan', unique=True)
    )

    idTrainplan: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    User_idUser: Mapped[int] = mapped_column(Integer, primary_key=True)

    User_: Mapped['User'] = relationship('User', back_populates='Trainplan')
    Trainday: Mapped[list['Trainday']] = relationship('Trainday', back_populates='Trainplan_')


class MealFood(Base):
    __tablename__ = 'Meal_Food'
    __table_args__ = (
        ForeignKeyConstraint(['Food_idFood'], ['Food.idFood'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Meal_Food_Food1'),
        ForeignKeyConstraint(['Meal_idMeal', 'Meal_User_idUser'], ['Meal.idMeal', 'Meal.User_idUser'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Meal_Food_Meal1'),
        Index('fk_Meal_Food_Food1_idx', 'Food_idFood'),
        Index('fk_Meal_Food_Meal1_idx', 'Meal_idMeal', 'Meal_User_idUser'),
        Index('idMeal_Food_UNIQUE', 'idMeal_Food', unique=True)
    )

    idMeal_Food: Mapped[int] = mapped_column(Integer, primary_key=True)
    grams: Mapped[decimal.Decimal] = mapped_column(DECIMAL(6, 2), nullable=False)
    Food_idFood: Mapped[int] = mapped_column(Integer, primary_key=True)
    Meal_idMeal: Mapped[int] = mapped_column(Integer, primary_key=True)
    Meal_User_idUser: Mapped[int] = mapped_column(Integer, primary_key=True)

    Food_: Mapped['Food'] = relationship('Food', back_populates='Meal_Food')
    Meal_: Mapped['Meal'] = relationship('Meal', back_populates='Meal_Food')


class Trainday(Base):
    __tablename__ = 'Trainday'
    __table_args__ = (
        ForeignKeyConstraint(['Trainplan_idTrainplan', 'Trainplan_User_idUser'], ['Trainplan.idTrainplan', 'Trainplan.User_idUser'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Trainday_Trainplan1'),
        Index('fk_Trainday_Trainplan1_idx', 'Trainplan_idTrainplan', 'Trainplan_User_idUser'),
        Index('idTrainday_UNIQUE', 'idTrainday', unique=True)
    )

    idTrainday: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    Trainplan_idTrainplan: Mapped[int] = mapped_column(Integer, primary_key=True)
    Trainplan_User_idUser: Mapped[int] = mapped_column(Integer, primary_key=True)

    Trainplan_: Mapped['Trainplan'] = relationship('Trainplan', back_populates='Trainday')
    Trainday_exercise: Mapped[list['TraindayExercise']] = relationship('TraindayExercise', back_populates='Trainday_')


class TraindayExercise(Base):
    __tablename__ = 'Trainday_exercise'
    __table_args__ = (
        ForeignKeyConstraint(['Exercise_idExercise'], ['Exercise.idExercise'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Trainday_exercise_Exercise1'),
        ForeignKeyConstraint(['Trainday_idTrainday', 'Trainday_Trainplan_idTrainplan', 'Trainday_Trainplan_User_idUser'], ['Trainday.idTrainday', 'Trainday.Trainplan_idTrainplan', 'Trainday.Trainplan_User_idUser'], ondelete='CASCADE', onupdate='CASCADE', name='fk_Trainday_exercise_Trainday1'),
        Index('fk_Trainday_exercise_Exercise1_idx', 'Exercise_idExercise'),
        Index('fk_Trainday_exercise_Trainday1_idx', 'Trainday_idTrainday', 'Trainday_Trainplan_idTrainplan', 'Trainday_Trainplan_User_idUser'),
        Index('idTrainday_exercise_UNIQUE', 'idTrainday_exercise', unique=True)
    )

    idTrainday_exercise: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numSets: Mapped[int] = mapped_column(Integer, nullable=False)
    Exercise_idExercise: Mapped[int] = mapped_column(Integer, primary_key=True)
    Trainday_idTrainday: Mapped[int] = mapped_column(Integer, primary_key=True)
    Trainday_Trainplan_idTrainplan: Mapped[int] = mapped_column(Integer, primary_key=True)
    Trainday_Trainplan_User_idUser: Mapped[int] = mapped_column(Integer, primary_key=True)
    notes: Mapped[Optional[str]] = mapped_column(String(45))

    Exercise_: Mapped['Exercise'] = relationship('Exercise', back_populates='Trainday_exercise')
    Trainday_: Mapped['Trainday'] = relationship('Trainday', back_populates='Trainday_exercise')
    Set: Mapped[list['Set']] = relationship('Set', back_populates='Trainday_exercise')


class Set(Base):
    __tablename__ = 'Set'
    __table_args__ = (
        ForeignKeyConstraint(['Trainday_exercise_idTrainday_exercise'], ['Trainday_exercise.idTrainday_exercise'], ondelete='RESTRICT', onupdate='RESTRICT', name='fk_Set_Trainday_exercise1'),
        Index('fk_Set_Trainday_exercise1_idx', 'Trainday_exercise_idTrainday_exercise'),
        Index('idSet_UNIQUE', 'idSet', unique=True)
    )

    idSet: Mapped[int] = mapped_column(Integer, primary_key=True)
    weight: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    Trainday_exercise_idTrainday_exercise: Mapped[int] = mapped_column(Integer, primary_key=True)

    Trainday_exercise: Mapped['TraindayExercise'] = relationship('TraindayExercise', back_populates='Set')
