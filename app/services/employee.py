from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas
from app.OAuth2 import hash_password
from app.enums.emailTemplate import EmailTemplate
from app.services import auth
from app.utilities import div_ciel, send_mail
from app.enums import AccountStatus, Role
from app.dependencies import PaginationParams


def convert_employee_to_schema(employee: models.Employee):
    return schemas.EmployeeOut(
        id=employee.id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        number=employee.number,
        birth_date=employee.birth_date,
        address=employee.address,
        cnss_number=employee.cnss_number,
        contract_type=employee.contract_type,
        gender=employee.gender,
        phone_number=employee.phone_number,
        roles=[employee_role.role for employee_role in employee.roles],
        account_status=employee.account_status,
        created_at=employee.created_at,
    )

def get_all(db: Session, pg_params: PaginationParams):
    skip = pg_params.limit * (pg_params.page - 1)
    query = db.query(models.Employee)
    if pg_params.name:
        query = query.filter(func.lower(func.concat(models.Employee.first_name, " ", models.Employee.last_name)).contains(func.lower(pg_params.name)))
    total_records = query.count()
    total_pages = div_ciel(total_records, pg_params.limit)
    result = query.limit(pg_params.limit).offset(skip).all()
    return schemas.EmployeesOut(
            list=[convert_employee_to_schema(emp) for emp in result],
            total_records=total_records,
            total_pages=total_pages,
            page_number=pg_params.page,
            page_size=pg_params.limit,
            detail="Employees fetched",
            status_code=200,
        )

def update_roles(roles: List[Role], db: Session, employee_id: int):
    try:
        query = db.query(models.EmployeeRole.role).filter(models.EmployeeRole.employee_id == employee_id)
        current_roles = {role[0] for role in query.all()}
        new_roles = {role for role in roles}
        roles_to_delete = current_roles - new_roles
        roles_to_add = new_roles - current_roles
        if roles_to_delete:
            db.query(models.EmployeeRole).filter(models.EmployeeRole.employee_id == employee_id,models.EmployeeRole.role.in_(roles_to_delete),).delete()
        if roles_to_add:
            db.add_all([models.EmployeeRole(role=role, employee_id=employee_id)for role in roles_to_add])
            return True
    except Exception as error:
        return schemas.BaseOut(status_code=400, detail=str(error))

def get_by_id(id: int, db: Session):
    return db.query(models.Employee).filter(models.Employee.id == id).first()

def sudo_edit_employee(id: int, new_data: dict, db: Session):
    return db.query(models.Employee).filter(models.Employee.id == id).update(new_data)

def get_by_email(email: str, db: Session):
    return db.query(models.Employee).filter(models.Employee.email == email).first()

async def add(employee_dict: dict, db: Session):
    roles = employee_dict.pop("roles")
    new_emp = models.Employee(**employee_dict)
    db.add(new_emp)
    db.flush()
    db.add_all([models.EmployeeRole(role=role, employee_id=new_emp.id) for role in roles])
    confirmation_code = auth.add_confirmation_code(new_emp.id, new_emp.email, db)
    await send_mail(
        schemas.MailData(
            emails=[new_emp.email],
            body={"name": f"{new_emp.first_name} {new_emp.last_name}","token": confirmation_code.token},
            template=EmailTemplate.ConfirmAccountTemplate,
            subject="Confirm Account",
        )
    )
    db.commit()
    return new_emp

async def update(employee_id: int, fields_to_update: dict, db: Session):
    employee_to_update = get_by_id(employee_id, db)
    if employee_to_update is None:
        return schemas.BaseOut(status_code=404, detail="Employee not found")
    {fields_to_update.pop(key, None) for key in ["confirm_password", "actual_password"]}
    if fields_to_update["password"] != None:
        fields_to_update["password"] = hash_password(fields_to_update["password"])
    else:
        fields_to_update.pop("password", None)
    if fields_to_update["roles"] != None:
        update_roles(fields_to_update["roles"], db, employee_to_update.id)
    fields_to_update.pop("roles", None)
    last_email = employee_to_update.email
    sudo_edit_employee(employee_to_update.id, fields_to_update, db)
    db.flush()
    db.refresh(employee_to_update)
    if employee_to_update.email != last_email:
        new_code = auth.add_confirmation_code(employee_to_update.id, employee_to_update.email, db)
        await send_mail(
            schemas.MailData(
                emails=[employee_to_update.email],
                body={"name": f"{employee_to_update.first_name} {employee_to_update.last_name}","code": new_code.token},
                template=EmailTemplate.ConfirmEmailTemplate,
                subject="Confirm Email",
            )
        )
        employee_to_update.account_status = AccountStatus.Inactive
    db.commit()
    return employee_to_update


def delete(id: int, db: Session):
    deleted_employee = db.query(models.Employee).filter(models.Employee.id == id).delete()
    db.commit()
    return deleted_employee
