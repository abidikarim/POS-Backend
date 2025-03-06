from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.dependencies import PaginationParams
from app.utilities import div_ciel


def get(db: Session, pg_params: PaginationParams):
    skip = pg_params.limit * (pg_params.page - 1)
    query = db.query(models.Pricelist)
    if pg_params.name and pg_params.name != "":
        query = query.filter(func.lower(func.concat(models.Pricelist.name + " " + models.Pricelist.description)).contains(func.lower(pg_params.name)))
    total_records = query.count()
    total_pages = div_ciel(total_records, pg_params.limit)
    result = query.limit(pg_params.limit).offset(skip).all()
    return {"total_records": total_records, "total_pages": total_pages, "list": result}


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


def delete(db: Session, id: int):
    pricelist_deleted = db.query(models.Pricelist).filter(models.Pricelist.id == id).delete()
    db.commit()
    return pricelist_deleted
