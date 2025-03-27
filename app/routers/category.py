from fastapi import APIRouter, File, UploadFile
from app import schemas
from app.dependencies import dbDep, currentEmployee, pagination_params,categorySchema
from app.services import category
from app.services.error import add_error,get_error_detail

router = APIRouter(prefix="/category", tags=["Category"])

error_keys={
    "categories_pkey":{"message":"Category not found","status":404},
}

@router.get("")
def get_all(db: dbDep, pg_params: pagination_params, curr_emp: currentEmployee):
    try:
        data = category.get(db, pg_params)
        return schemas.CategoriesOut(
            total_records=data["total_records"],
            total_pages=data["total_pages"],
            page_number=pg_params.page or 1,
            page_size=pg_params.limit or data["total_records"],
            list=data["list"],
            detail="Categories fetched",
            status_code=200,
        )
    except Exception as error:
        return schemas.BaseOut(status_code=400, detail=str(error))

@router.get("/{id}")
def get_one(db: dbDep, id: int, curr_emp: currentEmployee):
    try:
        category_db = category.get_by_id(db, id)
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.CategoryOut.model_validate(category_db)

@router.post("")
def create_category(db: dbDep, category_data: categorySchema , curr_emp: currentEmployee,category_image:UploadFile = File(...)):
    try:
        category.add(db, category_data.model_dump(),category_image)
    except Exception as error:
        db.rollback()
        add_error(str(error), db)
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=201, detail="Category created")

@router.put("/{id}")
def edit_category(db: dbDep, id: int, new_data: categorySchema, cur_emp: currentEmployee,category_image:UploadFile =File(None)):
    try:
        updated_category = category.edit(db, id, new_data.model_dump(),category_image)
        if not updated_category:
            return schemas.BaseOut(status_code=404,detail="Category not found")
    except Exception as error:
        add_error(str(error), db)
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=200, detail="Category updated")

@router.delete("/{id}")
def delete_category(db: dbDep, id: int, curr_emp: currentEmployee):
    try:
        deleted_category = category.delete(db,id)
        if not deleted_category:
            return schemas.BaseOut(status_code=404,detail="Category not found")
        category.delete(db, id)
        db.commit()
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=200, detail="Category deleted")
