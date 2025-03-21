from typing import List
from fastapi import APIRouter
from app.dependencies import dbDep,  currentEmployee
from app.services import pricelist
from app import schemas
from app.services.error import get_error_detail
router = APIRouter(prefix="/pricelist", tags=["Pricelist"])

error_keys={
    "pricelists_pkey":{"message":"Pricelist not found","status":404}
}
@router.get("",response_model=List[schemas.PricelistOut])
def get_all(db: dbDep,curr_emp:currentEmployee):
    try:
        return pricelist.get(db)
    except Exception as error:
        error_detail =get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])


@router.post("")
def create_pricelist(db: dbDep, pricelist_data: schemas.PricelistBase,curr_emp:currentEmployee):
    try:
        new_pricelist = pricelist.add(db, pricelist_data.model_dump())
        if new_pricelist:
            return schemas.BaseOut(status_code=201, detail="Pricelist created")
    except Exception as error:
         error_detail =get_error_detail(str(error),error_keys)
         return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])


@router.put("/{id}")
def edit_pricelist(db: dbDep, pricelist_data: schemas.PricelistBase, id: int,curr_emp:currentEmployee):
    try:
        updated_pricelist = pricelist.update(db, pricelist_data.model_dump(), id)
        if not updated_pricelist:
            return schemas.BaseOut(status_code=404, detail="Pricelist not found")
    except Exception as error:
        error_detail =get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=200, detail="Pircelist updated")

