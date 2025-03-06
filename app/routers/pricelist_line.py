from typing import List
from fastapi import APIRouter
from app import schemas
from app.services import pricelist_line
from app.dependencies import dbDep
from app.services.error import get_error_detail

router = APIRouter(prefix="/pricelistline", tags=["PricelistLine"])

error_keys={
    "pricelist_lines_pkey":{"message":"Pricelist line not found","status":404},
    "pricelist_lines_pricelist_id_fkey" :{"message":"Pricelist not found","status":404},
    "pricelist_lines_product_id_fkey":{"message":"Product not found","status":404},
    "pricelist_lines_check":{"message":"start_date must be before end_date ","status":400}
}


@router.get("/", response_model=List[schemas.PricelistLineOut])
def get_pricelist_line(db: dbDep):
    try:
        pricelist_lines = pricelist_line.get(db)
        return pricelist_lines
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])


@router.post("/")
def create_pricelist_line(db: dbDep, data: schemas.PricelistLineBase):
    try:
        new_pricelist_line = pricelist_line.add(db, data.model_dump())
    except Exception as error:
        error_detail =get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=201, detail="Pricelist line created ")


@router.put("/{id}")
def update_pricelist_line(db: dbDep, data: schemas.PricelistLineBase, id: int):
    try:
        updated_pricelist_line = pricelist_line.update(db, data.model_dump(), id)
        if not updated_pricelist_line:
            return schemas.BaseOut(status_code=404,detail="Pricelist line not found")
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=200, detail="Pricelist line updated")


@router.delete("/{id}")
def delete_pricelist_line(db: dbDep, id: int):
    try:
        deleted_pricelist_line  =pricelist_line.delete(db, id)
        if not deleted_pricelist_line:
            return schemas.BaseOut(status_code=200, detail="Pricelist line not found")
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=200, detail="Pricelist line deleted")
    
