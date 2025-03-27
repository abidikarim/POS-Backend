from fastapi import APIRouter
from app.dependencies import dbDep,order_filter
from app.services import order
from app import schemas
from app.services.error import get_error_detail

router=APIRouter(prefix="/order",tags=['Order'])

error_keys={}

@router.get("")
def get_all(db:dbDep,pg_params:order_filter):
    try:
        return order.get(db,pg_params)
    except Exception as error:
        return schemas.BaseOut(status_code=400,detail=str(error))
    
@router.post("")
def create(db:dbDep,data:schemas.OrderBase):
    try:
        new_order= order.add(db,data.model_dump())
        if new_order:
            return schemas.BaseOut(detail="Order created successfuly",status_code=201)
    except Exception as error:
        error_detail= get_error_detail(str(error),error_keys)
        return schemas.BaseOut(detail=error_detail["message"],status_code=error_detail["status"])
    
# @router.put("/{id}")
# def update(db:dbDep,data:)