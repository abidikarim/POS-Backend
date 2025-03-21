from sqlalchemy.orm import Session,joinedload
from app import models

def get(db: Session):
   pricelists = db.query(models.Pricelist).options(joinedload(models.Pricelist.pricelist_lines)).all()
   return pricelists

def get_by_id(db: Session, id: int):
    return db.query(models.Pricelist).filter(models.Pricelist.id == id).first()

def add(db: Session, pricelist: dict):
    new_pricelist = models.Pricelist(**pricelist)
    db.add(new_pricelist)
    db.commit()
    db.refresh(new_pricelist)
    return new_pricelist

def update(db: Session, pricelist_data: dict, id: int):
    pricelist_updated =db.query(models.Pricelist).filter(models.Pricelist.id == id).update(pricelist_data, synchronize_session=False)
    db.commit()
    return pricelist_updated