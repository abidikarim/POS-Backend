from fastapi import APIRouter, BackgroundTasks
from app.dependencies import dbDep, currentEmployee
from app.services import upload_employee
from app import schemas

router = APIRouter()


@router.get("/possibleImportFields")
def get_fields(cur_emp: currentEmployee):
    return upload_employee.get_possible_fields()


@router.post("/upload")
def upload_employees(entry: schemas.UploadEntry,bg_tasks: BackgroundTasks,db: dbDep,cur_emp: currentEmployee):
    return upload_employee.upload(entry, bg_tasks, db)
