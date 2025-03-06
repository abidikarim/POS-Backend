import cloudinary.uploader
from fastapi import UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import enums, models, schemas
from app.dependencies import ProductFilter
from app.utilities import div_ciel
from app.services import category

mandatory_fields = {
    "name": "Name",
    "description": "Description",
    "price": "Price",
    "quantity": "Quantity",
    "image_link": "Image",
    "category_id": "Category",
}


def is_positive(field):
    try:
        res = int(field)
    except:
        return None
    return res if res > 0 else None


def is_valid_category(field, categories):
    for field in categories:
        return categories[field]
    return None

def get(db: Session, pg_params: ProductFilter):
    skip = pg_params.limit * (pg_params.page - 1)
    query = db.query(models.Product)
    if pg_params.name :
        query = query.filter(func.lower(models.Product.name).contains(func.lower(pg_params.name)))
    if pg_params.category :
        query = query.join(models.Category).filter(func.lower(models.Category.name).contains(func.lower(pg_params.category)))
    if pg_params.max_price > 0:
        query = query.filter(models.Product.price <= pg_params.max_price)
    if pg_params.min_price > 0:
        query = query.filter(models.Product.price >= pg_params.min_price)
    if pg_params.max_quantity > 0:
        query = query.filter(models.Product.quantity <= pg_params.max_quantity)
    if pg_params.min_quantity > 0:
        query = query.filter(models.Product.quantity >= pg_params.min_quantity)
    total_records = query.count()
    total_pages = div_ciel(total_records, pg_params.limit)
    result = query.limit(pg_params.limit).offset(skip).all()
    return {"total_records": total_records, "total_pages": total_pages, "list": result}


def get_by_id(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.id == id).first()


def edit(db: Session, id: int, new_data: dict,product_image:UploadFile):
    try:
        if product_image and product_image.file:
            product_db = get_by_id(db,id)
            if product_db.public_id:
                cloudinary.uploader.destroy(product_db.public_id)
            image_data = cloudinary.uploader.upload(product_image.file)
            public_id = image_data.get("public_id")
            new_data.update({"image_link":image_data.get("secure_url"),"public_id":public_id})
        updated_product = db.query(models.Product).filter(models.Product.id == id).update(new_data, synchronize_session=False)
        db.commit()
        return updated_product
    except Exception as error:
        db.rollback()
        if public_id:
            cloudinary.uploader.upload(public_id)
        return schemas.BaseOut(status_code=400,detail="Somthing went wrong")


def add(db: Session, product: dict,image:UploadFile):
    try:
        new_product = models.Product(**product)
        image_data = cloudinary.uploader.upload(image.file)
        public_id = image_data.get("public_id")
        new_product.image_link = image_data.get("secure_url")
        new_product.public_id = public_id
        db.add(new_product)
        db.commit()
        return new_product
    except Exception as error:
        db.rollback()
        if public_id:
            cloudinary.uploader.destroy(public_id)
        return schemas.BaseOut(status_code=400,detail=str(error))


def fields(db: Session):
    categories_db = category.get(db)
    categories = {c.name.strip().lower() for c in categories_db}
    options = [
        schemas.MatchyOption(
            display_value=mandatory_fields["name"],
            value="name",
            mandatory=True,
            type=enums.FieldType.string,
        ),
        schemas.MatchyOption(
            display_value=mandatory_fields["description"],
            value="description",
            mandatory=True,
            type=enums.FieldType.string,
        ),
        schemas.MatchyOption(
            display_value=mandatory_fields["price"],
            value="price",
            mandatory=True,
            type=enums.FieldType.float,
            conditions=[
                schemas.MatchyCondition(
                    property=enums.ConditionProperty.value,
                    comparer=enums.MatchyComparer.gt,
                    value=0,
                )
            ],
        ),
        schemas.MatchyOption(
            display_value=mandatory_fields["quantity"],
            value="quantity",
            mandatory=True,
            type=enums.FieldType.integer,
            conditions=[
                schemas.MatchyCondition(
                    property=enums.ConditionProperty.value,
                    comparer=enums.MatchyComparer.gt,
                    value=0,
                )
            ],
        ),
        schemas.MatchyOption(
            display_value=mandatory_fields["image_link"],
            value="image_link",
            mandatory=True,
            type=enums.FieldType.file,
        ),
        schemas.MatchyOption(
            display_value=mandatory_fields["category_id"],
            value="category_id",
            mandatory=True,
            type=enums.FieldType.string,
            conditions=[
                schemas.MatchyCondition(
                    property=enums.ConditionProperty.value,
                    comparer=enums.MatchyComparer._in,
                    value=categories,
                )
            ],
        ),
    ]
    return schemas.ImportPossibleFields(possible_fields=options)

async def upload(db: Session, entry: schemas.UploadEntry):
    products = entry.lines
    categories_db = category.get(db)
    categories = {c.name.strip().lower(): c.id for c in categories_db}
    products_to_add = []
    for product in products:
        product_to_add = {field: cell.value for field, cell in product.items()}
        product_to_add["category_id"] = categories[product_to_add["category_id"]]
        products_to_add.append(models.Product(**product_to_add))
    # fields_check = {
    #     "price": (lambda field: is_positive(field), "Price must be positive"),
    #     "quantity": (lambda field: is_positive(field), "Quantity should be positive"),
    #     "category": (
    #         lambda field: is_valid_category(field, categories),
    #         f"Possible categories are : {categories.keys()}",
    #     ),
    # }
    missing_mandatory_fields = set(mandatory_fields.keys()) - products[0].keys()
    if missing_mandatory_fields:
        fields_name = [mandatory_fields[field] for field in missing_mandatory_fields]
        return schemas.BaseOut(status_code=400,detail=f"Missing Mandatory Fields : {(', ').join(fields_name)}")
    try:
        db.add_all(products_to_add)
        db.commit()
        return schemas.BaseOut(status_code=201, detail="File uploaded successfuly")
    except Exception as error:
        return schemas.BaseOut(status_code=400, detail=str(error))


def delete(db: Session, id: int):
   deleted_product = db.query(models.Product).filter(models.Product.id == id).delete()
   db.commit()
   return deleted_product
