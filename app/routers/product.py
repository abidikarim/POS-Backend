from fastapi import APIRouter, File, UploadFile
from app import schemas
from app.dependencies import dbDep, currentEmployee,productSchema,product_filter
from app.services import product
from app.services.error import add_error, get_error_detail

error_keys = {
    "products_category_id_fkey": {"status": 400,"message": "Category has this id not found"},
    "products_pkey":{"message":"Product not found","status":404}
    }

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("/")
def get_all(db: dbDep, pg_params: product_filter, cur_emp: currentEmployee):
    try:
        data = product.get(db, pg_params)
    except Exception as error:
        return schemas.BaseOut(status_code=400, detail=str(error))
    return schemas.ProductsOut(
        total_records=data["total_records"],
        total_pages=data["total_pages"],
        page_number=pg_params.page,
        page_size=pg_params.limit,
        list=data["list"],
        detail="Products fetched",
        status_code=200,
    )

@router.get("/fields")
def possible_fields(db: dbDep, cur_emp: currentEmployee):
    try:
        return product.fields(db)
    except Exception as error:
        error_detail = get_error_detail(str(error), error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])

@router.get("/{id:int}")
def get_one(db: dbDep, id: int, cur_emp: currentEmployee):
    try:
       product_db = product.get_by_id(db,id)
       if not product_db:
           return schemas.BaseOut(status_code=404,detail="Product not found")
    except Exception as error:
        error_detail = get_error_detail(str(error), error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.ProductOut.model_validate(product_db)

@router.post("/")
async def create_product(db: dbDep, product_data:  productSchema , cur_emp: currentEmployee,product_image:UploadFile = File(...)): 
    try:
        new_product = product.add(db, product_data.model_dump(),product_image)
    except Exception as error:
        add_error(str(error), db)
        error_detail = get_error_detail(str(error), error_keys)
        return schemas.BaseOut(status_code=error_detail["status"], detail=error_detail["message"])
    return schemas.BaseOut(status_code=201, detail="Product created")

@router.put("/{id}")
def edit_product(db: dbDep, id: int, new_data: productSchema, cur_emp: currentEmployee,product_image:UploadFile=File(None)):
    try:
        updated_product  =product.edit(db, id, new_data.model_dump(),product_image)
        if not updated_product:
            return schemas.BaseOut(status_code=404,detail="Product not found")
    except Exception as error:
        db.rollback()
        add_error(str(error), db)
        return schemas.BaseOut(status_code=400, detail=str(error))
    return schemas.BaseOut(status_code=200, detail="Product updated")

@router.delete("/{id}")
def delete_product(db: dbDep, id: int, cur_emp: currentEmployee):
    try:
        deleted_product =  product.delete(db, id)
        if not deleted_product:
             return schemas.BaseOut(status_code=404, detail="Product not found")
    except Exception as error:
        return schemas.BaseOut(status_code=400, detail=str(error))
    return schemas.BaseOut(status_code=200, detail="Product deleted")

@router.post("/upload")
async def upload(db: dbDep, entry: schemas.UploadEntry):
    try:
        return await product.upload(db, entry)
    except Exception as error:
        return schemas.BaseOut(status_code=400, detail=str(error))
