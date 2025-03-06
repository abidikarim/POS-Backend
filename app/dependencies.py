import json
from fastapi import Depends, Form, Query
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from app import models,schemas
from app.OAuth2 import get_current_employee
from app.database import get_db
from sqlalchemy.orm import Session

dbDep = Annotated[Session, Depends(get_db)]
formDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]

def get_product_schema (product_data:str =Form(...))->schemas.ProductBase:
    product_data= json.loads(product_data)
    return schemas.ProductBase(**product_data)

def get_category_schema(category_data:str = Form(...))->schemas.CategoryBase:
    category_data = json.loads(category_data)
    return schemas.CategoryBase(**category_data)

categorySchema = Annotated[schemas.CategoryBase,Depends(get_category_schema)]
productSchema = Annotated[schemas.ProductBase,Depends(get_product_schema)]

class PaginationParams(BaseModel):
      name :Optional[str]=""
      page:int=1
      limit:int=10

class ProductFilter(PaginationParams):
       category:str=""
       min_price :float =0
       max_price :float =0
       min_quantity :int=0
       max_quantity: int =0


product_filter = Annotated[ProductFilter, Depends()]
pagination_params = Annotated[PaginationParams, Depends()]
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
tokenDep = Annotated[str, Depends(oauth_scheme)]

def get_curr_emp(db: dbDep, token: tokenDep):
    return get_current_employee(db, token)

currentEmployee = Annotated[models.Employee, Depends(get_curr_emp)]
