import uuid
from app.enums import TokenStatus
from sqlalchemy.orm import Session
from app import models

def get_confirmation_code(code: str, db: Session):
    confirmation_code = db.query(models.AccountActivation).filter(models.AccountActivation.token == code).first()
    return confirmation_code

def add_confirmation_code(employee_id: int, email: str, db: Session):
    confirmation_code = models.AccountActivation(
        employee_id=employee_id,
        token=uuid.uuid1(),
        email=email,
        status=TokenStatus.Pending,
    )
    db.add(confirmation_code)
    return confirmation_code

def edit_confirmation_code(code_id: int, db: Session):
    updated_code = db.query(models.AccountActivation).filter(models.AccountActivation.id == code_id).update({models.AccountActivation.status: TokenStatus.Used})
    return updated_code

def get_reset_code(code: str, db: Session):
    reset_code =  db.query(models.ResetPassword).filter(models.ResetPassword.token == code).first()
    return reset_code


def add_reset_code(employee_id: int, email: str, db: Session):
    reset_code = models.ResetPassword(
        employee_id=employee_id,
        email=email,
        token=uuid.uuid1(),
        status=TokenStatus.Pending,
    )
    db.add(reset_code)
    return reset_code

def edit_reset_code(code_id: int, db: Session):
   updated_reset_code =  db.query(models.ResetPassword).filter(models.ResetPassword.id == code_id).update({models.ResetPassword.status: TokenStatus.Used})
   return updated_reset_code