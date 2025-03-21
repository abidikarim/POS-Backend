from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models
from app.dependencies import PaginationParams
from app.utilities import div_ciel


def get(db:Session,pg_params:PaginationParams):
    skip = pg_params.limit * (pg_params.page - 1)
    query = db.query(models.Customer)
    if pg_params.name:
        query = query.filter(
            func.lower(
                func.concat(models.Customer.name, " ", models.Customer.email)
            ).contains(func.lower(pg_params.name))
        )
    total_records = query.count()
    total_pages = div_ciel(total_records, pg_params.limit)
    result = query.limit(pg_params.limit).offset(skip).all()
    return {
        "total_records": total_records,
        "total_pages": total_pages,
        "list": result,
    }

def get_by_id(db:Session,id:int):
    customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    return customer

def add(db:Session,data:dict):
    new_customer = models.Customer(**data)
    db.add(new_customer)
    db.commit()
    return new_customer

def edit(db:Session,data:dict,id:int):
    customer_updated = db.query(models.Customer).filter(models.Customer.id == id).update(data,synchronize_session=False)
    db.commit()
    return customer_updated

def delete(db:Session,id:int):
    customer_deleted = db.query(models.Customer).filter(models.Customer.id == id).delete()
    db.commit()
    return customer_deleted