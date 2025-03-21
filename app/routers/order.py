from fastapi import APIRouter
from app.dependencies import dbDep,order_filter
from app.services import order
from app import schemas
router=APIRouter(prefix="/order",tags=['Order'])

@router.get("")
def get_all(db:dbDep,pg_params:order_filter):
    try:
        return order.get(db,pg_params)
    except Exception as error:
        return schemas.BaseOut(status_code=400,detail=str(error))