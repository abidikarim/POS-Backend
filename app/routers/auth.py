from datetime import datetime
import uuid
from fastapi import APIRouter, status
from app import models, schemas
from app.OAuth2 import create_access_token, hash_password, verify_password
from app.dependencies import dbDep, formDataDep
from app.enums import AccountStatus, TokenStatus
from app.enums.emailTemplate import EmailTemplate
from app.services import auth, employee
from app.services.error import add_error
from app.utilities import send_mail

router = APIRouter(prefix="/auth", tags=["Authenticate"])


@router.post("/login")
def login(employee_credentials: formDataDep, db: dbDep):
    try:
        emp = employee.get_by_email(employee_credentials.username, db)
        if emp is None:
            return schemas.BaseOut(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
        if emp.account_status == AccountStatus.Inactive:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST,detail="Your account is inactive")
        if not verify_password(employee_credentials.password, emp.password):
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")
        access_token = create_access_token(data={"id": emp.id,"roles": [emp_role.role.value for emp_role in emp.roles]})
        return schemas.Token(access_token=access_token,token_type="Bearer",status_code=200,detail="Login success")
    except Exception as error:
        return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/forgotPassword")
async def forgot_password(entry: schemas.ForgotPassword, db: dbDep):
    try:
        emp = employee.get_by_email(entry.email, db)
        if emp is None:
            return schemas.BaseOut(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
        reset_code = auth.add_reset_code(employee_id=emp.id, email=emp.email, db=db)
        db.flush()
        await send_mail(
            schemas.MailData(
                emails=[emp.email],
                body={"name": f"{emp.first_name} {emp.last_name}","token": reset_code.token},
                template=EmailTemplate.ResetPasswordTemplate,
                subject="Reset Password",
            )
        )
        db.commit()
    except Exception as error:
        db.rollback()
        add_error(str(error), db)
        return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST,detail=str(error))
    return schemas.BaseOut(status_code=status.HTTP_200_OK, detail="Email send successfully")


@router.patch("/resetPassword")
def reset_password(entry: schemas.VerificationData, db: dbDep):
    try:
        if entry.password != entry.confirm_password:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST,detail="Passwords do not match ")
        reset_code = auth.get_reset_code(entry.code, db)
        if not reset_code:
            return schemas.BaseOut(status_code=status.HTTP_404_NOT_FOUND, detail="Link does not exist")
        if reset_code.status == TokenStatus.Used:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Link already used")
        if (datetime.now() - reset_code.created_at.replace(tzinfo=None)).days > 1:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Link expired")
        employee.sudo_edit_employee(reset_code.employee_id,{models.Employee.password: hash_password(entry.password)},db)
        auth.edit_reset_code(reset_code.id, db)
        db.commit()
    except Exception as error:
        db.rollback()
        add_error(text=str(error), db=dbDep)
        return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return schemas.BaseOut(status_code=status.HTTP_200_OK, detail="Password changed")


@router.patch("/confirmAccount")
def confirmation_account(entry: schemas.VerificationData, db: dbDep):
    try:
        if entry.password and  entry.password != entry.confirm_password:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
        confirmation_code = auth.get_confirmation_code(entry.code, db)
        if not confirmation_code:
            return schemas.BaseOut(status_code=status.HTTP_404_NOT_FOUND, detail="Link does not exist")
        if confirmation_code.status == TokenStatus.Used:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Link already used")
        if (datetime.now() - confirmation_code.created_at.replace(tzinfo=None)).days > 1:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Link expired")
        employee.sudo_edit_employee(confirmation_code.employee_id,{models.Employee.account_status: AccountStatus.Active,models.Employee.password: hash_password(entry.password)},db)
        auth.edit_confirmation_code(confirmation_code.id, db)
        db.commit()
    except Exception as error:
        db.rollback()
        add_error(text=str(error), db=db)
        return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return schemas.BaseOut(status_code=status.HTTP_200_OK, detail="Account confirmed")


@router.patch("/confirmEmail")
def confirmation_email(entry: schemas.confirmationCode, db: dbDep):
    try:
        confirmation_code = auth.get_confirmation_code(entry.code, db)
        if not confirmation_code:
            return schemas.BaseOut(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
        if confirmation_code.status == TokenStatus.Used:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Link already used")
        if (datetime.now() - confirmation_code.created_at.replace(tzinfo=None)).days > 1:
            return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Link expired")
        employee.sudo_edit_employee(confirmation_code.employee_id,{models.Employee.account_status: AccountStatus.Active},db)
        auth.edit_confirmation_code(confirmation_code.id, db)
        db.commit()
    except Exception as error:
        db.rollback()
        add_error(str(error), db)
        return schemas.BaseOut(status_code=status.HTTP_400_BAD_REQUEST, detail="Confirmation email failed")
    return schemas.BaseOut(status_code=status.HTTP_200_OK, detail="Email confirmed")