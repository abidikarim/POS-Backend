from fastapi import APIRouter
from app.services import customer
from app.dependencies import dbDep,pagination_params,currentEmployee
from app import schemas
from app.services.error import get_error_detail

router = APIRouter(prefix="/customer",tags=['Customer'])
error_keys={
    "customers_pkey":{"message":"Customer not found","status":404},
    "customers_pricelist_id_fkey":{"message":"Pricelist not found","status":404},
}

@router.get("")
def get_all(db:dbDep,pg_params:pagination_params,cur_emp:currentEmployee):
    try:
        data = customer.get(db,pg_params)
        return schemas.CustomersOut(
            list=data["list"],
            total_pages=data["total_pages"],
            total_records=data["total_records"],
            page_number=pg_params.page,
            page_size=pg_params.limit,
            status_code=200,
            detail="Customers fetched"
        )
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    
@router.post("")
def create(db:dbDep,data:schemas.Customer,cur_emp:currentEmployee):
    try:
        new_customer = customer.add(db,data.model_dump())
        if new_customer:
            return schemas.BaseOut(status_code=201,detail="Customer created")
    except Exception as error:
        db.rollback()
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])

@router.put("/{id}")
def update(db:dbDep,data:schemas.Customer,id:int,cur_emp:currentEmployee):
    try:
        customer_updated=  customer.edit(db,data.model_dump(),id)
        if customer_updated:
            return schemas.BaseOut(status_code=200,detail="Customer updated")
    except Exception as error:
        db.rollback()
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])

@router.delete("/{id}")
def delete(db:dbDep,id:int,cur_emp:currentEmployee):
    try:
        customer_deleted = customer.delete(db,id)
        if customer_deleted:
            return schemas.BaseOut(status_code=200,detail="Customer deleted")
    except Exception as error:
        db.rollback()
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])