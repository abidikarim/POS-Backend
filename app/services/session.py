from sqlalchemy import func
from sqlalchemy.orm import Session,joinedload
from app.dependencies import PaginationParams
from app import models
from app.services.employee import convert_employee_to_schema
from app.utilities import div_ciel
from app import schemas


def get(db:Session,pg_params:PaginationParams):
    skip = pg_params.limit * (pg_params.page - 1)
    query = db.query(models.Session).options(joinedload(models.Session.employee)).join(models.Employee)
    if pg_params.name:
       query = query.filter(func.lower(func.concat(models.Employee.first_name, " ", models.Employee.last_name)).contains(func.lower(pg_params.name))) 
    total_records = query.count()
    total_pages = div_ciel(total_records, pg_params.limit)
    result = query.limit(pg_params.limit).offset(skip).all()
    return schemas.SessionsOut(
            list= [schemas.SessionOut(
                    id=session.id,
                    opened_at=session.opened_at,
                    closed_at=session.closed_at,
                    employee_id=session.employee_id,
                    status=session.status,
                    employee=convert_employee_to_schema(session.employee)) for session in result],
            total_records=total_records,
            total_pages=total_pages,
            page_number=pg_params.page,
            page_size=pg_params.limit,
            detail="Sessions fetched",
            status_code=200
        )

def get_by_id(db:Session,id:int):
    session = db.query(models.Session).filter(models.Session.id == id).first()
    return session

def add(db:Session,data:dict):
    new_session= models.Session(**data)
    db.add(new_session)
    db.commit()
    return new_session

def edit(db:Session,data:dict,id:int):
    session_updated= db.query(models.Session).filter(models.Session.id == id).update(data,synchronize_session=False)
    db.commit()
    return session_updated

def delete(db:Session,id:int):
    session_deleted=db.query(models.Session).filter(models.Session.id == id).delete()
    db.commit()
    return session_deleted
