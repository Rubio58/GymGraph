# services/measurement_service.py

from datetime import datetime
from typing import Dict, List
from repositories.measurement_repository import MeasurementRepository
from database import get_db

class MeasurementService:

    def __init__(self):
        self.repo = MeasurementRepository()    

    def get_meascats(self) -> List[Dict]:
        
        with get_db() as db:
            meascats=self.repo.get_all_meascats(db)
            meascats_list=[]
            for mc in meascats:
                meascats_list.append({
                    'idMeasCat': mc.idMeasCat,
                    'name': mc.name,
                    'unit':mc.unit
                })
        return meascats_list
    
    def get_measurements_by_cat(self, meascat_id:int, user_id:int) -> List[Dict]:
        
        with get_db() as db:
            measurements=self.repo.get_measurements_by_cat(db, meascat_id, user_id)
            measurements_list=[]
            for m in measurements:
                measurements_list.append({
                    'idMeas': m.idMeas,
                    'val': m.val,
                    'date': m.date
                })

            measurements_list.sort(key=lambda x: x['date'], reverse=True)  
        return measurements_list    
    
    def create_measurement(self, val:float, date:datetime, meascat_id:int, user_id:int):
        with get_db() as db:
            try:
                self.repo.create_measurement(db,val,date,meascat_id,user_id)
                return {
                    'success': True
                }
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}        
        return
    
    def get_meascat_unit(self, meascat_id: int) -> str:
        with get_db() as db:
            meascat = self.repo.get_meascat_by_id(db, meascat_id)
            return meascat.unit   
        
    def delete_measurement(self, meas_id:int):
        with get_db() as db:
            try:
                self.repo.delete_measurement(db,meas_id)
                db.commit()    
            except Exception as e:
                db.rollback()
                return {'success': False, 'error': str(e)}
        return                