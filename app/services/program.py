from sqlalchemy import func
from sqlalchemy.orm import Session
from app.dependencies import PaginationParams
from app import models
from app.utilities import div_ciel
from app.services import program_item


def get(pg_params:PaginationParams,db:Session):
    skip = pg_params.limit * (pg_params.page - 1)
    query = db.query(models.Program)
    if pg_params.name and pg_params.name != "":
        query = query.filter(func.lower(func.concat(models.Program.name + " " + models.Program.description)).contains(func.lower(pg_params.name)))
    total_records = query.count()
    total_pages = div_ciel(total_records, pg_params.limit)
    result = query.limit(pg_params.limit).offset(skip).all()
    return {
            "total_records": total_records,
            "total_pages": total_pages, 
            "list": result,
            "page_number":pg_params.page,
            "page_size":pg_params.limit,
            "status_code":200,
            "detail":"Programs fetched"
        }

def get_by_id(id:int , db:Session):
    return db.query(models.Program).filter(models.Program.id == id).first()

def add(program_data:dict,db:Session):
    items_count = program_data.pop("items_count")
    new_program = models.Program(**program_data)
    db.add(new_program)
    db.flush()
    db.refresh(new_program)
    if items_count:
        program_item.add(items_count,new_program.id,db)
    db.commit()
    return new_program

def edit(id:int,program_data:dict,db:Session):
    updated_program = db.query(models.Program).filter(models.Program.id == id).update(program_data,synchronize_session=False)
    db.commit()
    return updated_program

def delete(id:int,db:Session):
    deleted_program = db.query(models.Program).filter(models.Program.id == id).delete()
    db.commit()
    return deleted_program