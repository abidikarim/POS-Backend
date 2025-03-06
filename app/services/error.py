from typing import Optional

from fastapi import HTTPException

from app import models
from sqlalchemy.orm import Session


def get_error_detail(error: str, error_keys: dict):
    for err in error_keys:
        if err in error:
            return error_keys[err]
    return dict({"message": "Somthing went wrong", "status": 400})


def add_error(text: str, db: Session, employee_id: Optional[int] = None):
    if not isinstance(text, str):
        raise ValueError(f"Expected 'text' to be a string, got {type(text)}")
    try:
        error_db = models.Error(text=text, employee_id=employee_id)
        db.add(error_db)
        db.commit()
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
