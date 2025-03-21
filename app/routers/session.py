from fastapi import APIRouter
from app.dependencies import dbDep,pagination_params,currentEmployee
from app.services import session
from app import schemas
from app.services.error import get_error_detail

router = APIRouter(prefix="/session",tags=["Session"])
error_keys={
    "sessions_pkey":{"message":"Session not found","status":404},
    "sessions_employee_id_fkey":{"message":"Employee not found","status":404},
}
@router.get("")
def get_all(db:dbDep,pg_params:pagination_params):
    try:
       return session.get(db,pg_params)
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    
@router.post("")
def create(db:dbDep,data:schemas.Session):
    try:
        new_session = session.add(db,data.model_dump())
        if new_session:
            return schemas.BaseOut(status_code=201,detail="Session created")
    except Exception as error:
        db.rollback()
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    

@router.put("/{id}")
def update(db:dbDep,data:schemas.Session,id:int):
    try:
        session_updated= session.edit(db,data.model_dump(),id)
        if session_updated:
            return schemas.BaseOut(status_code=200,detail="Session updated")
    except Exception as error:
        db.rollback()
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])

@router.delete("/{id}")
def delete(db:dbDep,id:int):
    try:
        session_deleted= session.delete(db,id)
        if session_deleted:
            return schemas.BaseOut(status_code=200,detail="Session deleted")
    except Exception as error:
        db.rollback()
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
