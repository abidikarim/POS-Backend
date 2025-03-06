from sqlalchemy.orm import Session
from app import models


def get(db: Session):
    pricelist_lines = db.query(models.PricelistLine).all()
    return pricelist_lines


def get_by_id(db: Session, id: int):
    pricelist_line =db.query(models.PricelistLine).filter(models.PricelistLine.id == id).first()
    return pricelist_line


def add(db: Session, data: dict):
    new_pricelist_line = models.PricelistLine(**data)
    db.add(new_pricelist_line)
    db.commit()
    return new_pricelist_line


def update(db: Session, new_data: dict, id: int):
    updated_pricelist_line= db.query(models.PricelistLine).filter(models.PricelistLine.id == id).update(new_data, synchronize_session=False)
    db.commit()
    return updated_pricelist_line


def delete(db: Session, id: int):
    deleted_pricelist_line = db.query(models.PricelistLine).filter(models.PricelistLine.id == id).delete()
    db.commit()
    return deleted_pricelist_line