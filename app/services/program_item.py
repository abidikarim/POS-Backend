from sqlalchemy.orm import Session
from app import models
import uuid
from app.enums import ProgramItemType

def get_by_id(id:int,db:Session):
    item = db.query(models.ProgramItem).filter(models.ProgramItem.id == id).first()
    return item 

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
