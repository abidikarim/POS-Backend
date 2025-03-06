from fastapi import APIRouter
from app.dependencies import dbDep, pagination_params, currentEmployee
from app.services import pricelist
from app import schemas
from app.services.error import get_error_detail
router = APIRouter(prefix="/pricelist", tags=["Pricelist"])

error_keys={
    "pricelists_pkey":{"message":"Pricelist not found","status":404}
}
@router.get("/")
def get_all(db: dbDep, pg_params: pagination_params):
    try:
        data = pricelist.get(db, pg_params)
        return schemas.PricelistsOut(
            status_code=200,
            detail="pricelists fetched",
            total_pages=data["total_pages"],
            total_records=data["total_records"],
            list=data["list"],
            page_number=pg_params.page,
            page_size=pg_params.limit,
        )
    except Exception as error:
        error_detail =get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])


@router.post("/", response_model=schemas.PricelistOut)
def create_pricelist(db: dbDep, pricelist_data: schemas.PricelistBase):
    try:
        new_pricelist = pricelist.add(db, pricelist_data.model_dump())
        if new_pricelist:
            return schemas.BaseOut(status_code=201, detail="Pricelist created")
    except Exception as error:
         error_detail =get_error_detail(str(error),error_keys)
         return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])


@router.put("/{id}")
def edit_pricelist(db: dbDep, pricelist_data: schemas.PricelistBase, id: int):
    try:
        updated_pricelist = pricelist.update(db, pricelist_data.model_dump(), id)
        if not updated_pricelist:
            return schemas.BaseOut(status_code=404, detail="Pricelist not found")
    except Exception as error:
        error_detail =get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=200, detail="Pircelist updated")


@router.delete("/{id}")
def delete_pricelist(db: dbDep, id: int):
    try:
        deleted_pricelist = pricelist.delete(db, id)
        if not deleted_pricelist:
            return schemas.BaseOut(status_code=404, detail="Pricelist not found")
    except Exception as error:
        error_detail =get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=200, detail="Pricelist deleted")
