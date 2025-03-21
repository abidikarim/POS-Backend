from sqlalchemy.orm import Session,joinedload
from app import models
from app.services import program_item


def get(db:Session):
  programs= db.query(models.Program).options(joinedload(models.Program.items)).all()
  return programs

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