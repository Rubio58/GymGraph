# repositories/measurement_repository.py
from datetime import datetime
from models import MeasCat, Meas
from sqlalchemy.orm import Session

class MeasurementRepository:

    def get_all_meascats(self, db:Session):
        return db.query(MeasCat).all()
    
    def get_measurements_by_cat(self, db:Session, meascat_id:int, user_id:int):
        return db.query(Meas).filter(Meas.MeasCat_idMeasCat == meascat_id, Meas.User_idUser==user_id).all()
    
    def create_measurement(self, db:Session, val:float, date:datetime, meascat_id:int, user_id:int):
        meas=Meas(
            val=val,
            date=date,
            MeasCat_idMeasCat=meascat_id,
            User_idUser=user_id
        )
        db.add(meas)
        db.flush()
        return
    
    def get_meascat_by_id(self, db: Session, meascat_id: int):
        return db.query(MeasCat).filter(MeasCat.idMeasCat == meascat_id).first()    
    
    def delete_measurement(self, db:Session, meas_id:int):
        m=db.query(Meas).filter(Meas.idMeas == meas_id).first()
        db.delete(m)
        return