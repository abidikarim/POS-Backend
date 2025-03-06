from sqlalchemy.orm import Session
from app import models
from app.dependencies import PaginationParams
import uuid
from app.enums import ProgramItemType
from app.utilities import div_ciel



def get(program_id:int,pg_params:PaginationParams,db:Session):
    skip = pg_params.limit * (pg_params.page - 1)
    query = db.query(models.ProgramItem).filter(models.ProgramItem.program_id == program_id)
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
            "detail":"Items fetched"
        }


def add(items_count:int,program_id:int,db:Session):
    items_to_add=[]
    for i in range(items_count):
        new_item= models.ProgramItem(code=uuid.uuid1(),program_id =program_id,status= ProgramItemType.Active)
        items_to_add.append(new_item)
    db.add_all(items_to_add)
    db.flush()
    return items_to_add


def edit(item_data:dict,item_id:int,db:Session):
    updated_item = db.query(models.ProgramItem).filter(models.ProgramItem.id == item_id).update(item_data,synchronize_session=False)
    return updated_item



def delete(item_id:int,db:Session):
    deleted_item = db.query(models.ProgramItem).filter(models.ProgramItem.id == item_id).delete()
    return deleted_item
