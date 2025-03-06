from fastapi import APIRouter, status
from app.services import employee
from app import schemas
from app.dependencies import dbDep, pagination_params, currentEmployee
from app.services.error import add_error, get_error_detail

router = APIRouter(prefix="/employee", tags=["Employee"])

error_keys = {
    "ck_employees_cnss_number": {"message": "-Cnss number it should be {8 digits}-{2 digits} and it's mandatory if contract type Cdi or Cdd","status": 400},
    "employees_email_key": {"message": "Email already used", "status": 409},
    "employees_number_key": {"message": "Number already used", "status": 409},
    "Username and Password not accepted": {"message": "Email credentials not accepted","status": 406},
    "employees_pkey": {"message": "Employee not found", "status": 404},
    "unique_employee_role": {"message": "This employee already has this role","status": 409},
    "employees_pkey":{"message":"Employee not found","status":404}
}


@router.get("/", response_model=schemas.EmployeesOut)
def get_employees(db: dbDep, pg_params: pagination_params, cur_emp: currentEmployee):
    try:
        data = employee.get_all(db=db, pg_params=pg_params)
        return schemas.EmployeesOut(
            list=[employee.convert_employee_to_schema(emp) for emp in data["list"]],
            total_records=data["total_records"],
            total_pages=data["total_pages"],
            page_number=pg_params.page,
            page_size=pg_params.limit,
            detail="Employees fetched",
            status_code=200,
        )
    except Exception as error:
        error_detail = get_error_detail(str(error), error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_employee(emp: schemas.EmployeeCreate, db: dbDep, cur_emp: currentEmployee):
    try:
        await employee.add(emp.model_dump(), db)
    except Exception as error:
        error_detail = get_error_detail(str(error), error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=201, detail="Employee added and email sent for confirmation")


@router.put("/{id}")
async def update_employee(update_data: schemas.EmployeeUpdate, id: int, db: dbDep, cur_emp: currentEmployee):
    try:
        if update_data.password != update_data.confirm_password:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be match")
        updated_employee = await employee.update(id, update_data.model_dump(), db)
        if not updated_employee:
            return schemas.BaseOut(status_code=404,detail="Employee not found")
    except Exception as error:
        db.rollback()
        error_detail = get_error_detail(str(error), error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=200, detail="Employee Updated")


@router.delete("/{id}")
def delete_employee(id: int, db: dbDep):
    try:
        deleted_employee = employee.delete(id, db)
        if not deleted_employee:
            return schemas.BaseOut(status_code=404,detail="Employee not found")
    except Exception as error:
        db.rollback()
        add_error(str(error), db)
        error_detail = get_error_detail(str(error), error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=200, detail="Employee Deleted")
