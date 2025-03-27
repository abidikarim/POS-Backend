from typing import List
from sqlalchemy.orm import Session
from app import models
from app import schemas

def edit(db:Session,data:dict,id:int):
    line_updated = db.query(models.OrderLine).filter(models.OrderLine.id == id).update(data,synchronize_session=False)
    db.commit()
    return line_updated

def delete(db:Session,id:int):
    line_deleted = db.query(models.OrderLine).filter(models.OrderLine.id == id).delete()
    db.commit()
    return line_deleted