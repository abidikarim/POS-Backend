from fastapi import APIRouter
from app.dependencies import dbDep,pagination_params
from app.services import program_item
from app.services.error import get_error_detail
from app import schemas

router = APIRouter(prefix="/programItem",tags=['Program Item'])

error_keys={
    "program_items_pkey":{"message":"Item not found","status":404},
    "program_items_program_id_fkey":{"message":"Program not found","status":404},
}

@router.get("/")
def get_items(program_id:int,pg_params:pagination_params,db:dbDep):
    try:
        program_items = program_item.get(program_id,pg_params,db)
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    return schemas.ProgramItemsOut.model_validate(program_items)


@router.put("/{id}")
def update_item(item_data:schemas.ProgramItemBase,id:int,db:dbDep):
    try:
        updated_item = program_item.edit(item_data.model_dump(),id,db)
        if not updated_item:
            return schemas.BaseOut(status_code=404,detail="Item not found")
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    return schemas.BaseOut(status_code=200,detail="Item updated")


@router.delete("/{id}")
def delete_item(id:int,db:dbDep):
    try:
        deleted_item = program_item.delete(id,db)
        if not deleted_item:
            return schemas.BaseOut(status_code=404,detail="Item not found")
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    return schemas.BaseOut(status_code=200,detail="Item deleted")