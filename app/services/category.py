import cloudinary.uploader

from fastapi import UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import PaginationParams
from app.utilities import div_ciel

def get(db: Session, pg_params: PaginationParams = None):
    if pg_params is None:
        return db.query(models.Category).all()
    query = db.query(models.Category)
    if pg_params.name != None and pg_params.name != "":
        query = query.filter(
            func.lower(
                func.concat(models.Category.name, " ", models.Category.description)
            ).contains(func.lower(pg_params.name))
        )
    if pg_params.limit:
        query = query.limit(pg_params.limit)
    if pg_params.page:
         skip = pg_params.limit * (pg_params.page - 1)
         query = query.offset(skip)
    total_records = query.count()
    total_pages = div_ciel(total_records, pg_params.limit)
    result = query.all()
    return {"total_records": total_records, "total_pages": total_pages, "list": result}

def get_by_id(db: Session, id: int):
    return db.query(models.Category).filter(models.Category.id == id).first()

def edit(db: Session, id: int, new_data: dict,category_image:UploadFile):
    try:
        if category_image and category_image.file:
            category_db= get_by_id(db,id)
            if category_db.public_id:
                cloudinary.uploader.destroy(category_db.public_id)
            image_data = cloudinary.uploader.upload(category_image.file)
            public_id = image_data.get("public_id")
            new_data.update({"public_id":public_id,"image_link":image_data.get("secure_url")})
        updated_category = db.query(models.Category).filter(models.Category.id == id).update(new_data,synchronize_session=False)
        db.commit()
    except Exception as error:
        db.rollback()
        if public_id:
            cloudinary.uploader.destroy(public_id)
        return schemas.BaseOut(status_code=400,detail="Somthing went wrong")
    return updated_category

def add(db: Session, category: dict,category_image:UploadFile):
   try:
        new_category = models.Category(**category)
        image_data = cloudinary.uploader.upload(category_image.file)
        public_id = image_data.get("public_id")
        new_category.image_link = image_data.get("secure_url")
        new_category.public_id = public_id
        db.add(new_category)
        db.commit()
        return new_category
   except Exception as error:
       db.rollback()
       if public_id:
           cloudinary.uploader.destroy(public_id)
       return schemas.BaseOut(status_code=400,detail="Somthing went wrong")


def delete(db: Session, id: int):
    deleted_category = db.query(models.Category).filter(models.Category.id == id).delete()
    return deleted_category
