from fastapi import APIRouter
from app import schemas
from app.dependencies import dbDep, currentEmployee, pagination_params
from app.services import program
from app.services.error import  get_error_detail

error_keys={
    "programs_product_to_buy_id_fkey":{"message":"Product to buy not found","status":404},
    "programs_product_to_get_id_fkey":{"message":"Product to get not found","status":404},
    "valid_program_date":{"message":"start_date must be before end_date"},
    "program_type_constraints":{"message":"Set discount with no products. Or set product_to_buy and product_to_get_id with no discount.","status":400},
    "programs_pkey":{"message":"Program not found","status":404}
}

router = APIRouter(prefix="/program",tags=["Program"])

@router.get("/",response_model=schemas.ProgramsOut)
def get_programs(pg_params:pagination_params,db:dbDep,cur_emp:currentEmployee):
    try:
        data = program.get(pg_params,db)
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    return schemas.ProgramsOut(**data)

@router.post("/")
def create_program(program_data:schemas.ProgramCreate,db:dbDep,cur_emp:currentEmployee):
    try:
        new_program = program.add(program_data.model_dump(),db)
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    return schemas.ProgramOut.model_validate(new_program)


@router.put("/{id:int}")
def update_program(program_data:schemas.ProgramUpdate,id:int,db:dbDep,cur_emp:currentEmployee):
    try:
        updated_program = program.edit(id,program_data.model_dump(),db)
        if not updated_program:
            return schemas.BaseOut(status_code=404,detail="Program not found")
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    return schemas.BaseOut(status_code=200,detail="Program updated")

@router.delete("/{id}")
def delete_program(id:int,db:dbDep,cur_emp:currentEmployee):
    try:
        deleted_program = program.delete(id,db)
        if not deleted_program:
            return schemas.BaseOut(status_code=404,detail="Program not found")
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    return schemas.BaseOut(status_code=200,detail="Program deleted")