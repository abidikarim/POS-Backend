from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from app.enums import Gender,AccountStatus,ContractType,Role,FieldType,MatchyComparer,ConditionProperty,ProgramType,ProgramItemType
from typing import List, Dict, Any, Optional
from app.enums.emailTemplate import EmailTemplate


class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class BaseOut(OurBaseModel):
    detail: str
    status_code: int

class PagedResponse(BaseOut):
    page_number: int
    page_size: int
    total_pages: int
    total_records: int

class EmployeeBase(OurBaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    number: int
    birth_date: date | None = None
    address: str | None = None
    cnss_number: str | None = None
    contract_type: ContractType
    gender: Gender
    phone_number: str | None = None
    roles: List[Role]

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    password: str | None = None
    confirm_password: str | None = None

class EmployeeOut(EmployeeBase):
    id: int
    account_status: AccountStatus
    created_at: datetime

class EmployeesOut(PagedResponse):
    list: List[EmployeeOut]

class ForgotPassword(OurBaseModel):
    email: EmailStr

class Token(BaseOut):
    access_token: str
    token_type: str

class PayloadData(OurBaseModel):
    id: int
    roles: List[Role]

class MailData(OurBaseModel):
    emails: List[EmailStr]
    body: Dict[str, Any]
    template: EmailTemplate
    subject: str

class VerificationData(OurBaseModel):
    password: str
    confirm_password: str
    code: str

class confirmationCode(OurBaseModel):
    code: str

class MatchyCondition(OurBaseModel):
    property: ConditionProperty
    comparer: Optional[MatchyComparer] = None
    value: int | float | str | List[str]
    custom_fail_message: Optional[str] = None

class MatchyOption(OurBaseModel):
    display_value: str
    value: Optional[str] = None
    mandatory: Optional[bool] = False
    type: FieldType
    conditions: Optional[List[MatchyCondition]] = []

class ImportPossibleFields(OurBaseModel):
    possible_fields: List[MatchyOption] = []

class MatchyCell(OurBaseModel):
    colIndex: int
    rowIndex: int
    value: str

class UploadEntry(OurBaseModel):
    lines: List[Dict[str, MatchyCell]]
    force_upload: Optional[bool] = False

class MatchyWrongCell(OurBaseModel):
    message: str
    rowIndex: int
    colIndex: int

class ImportResponse(BaseOut):
    errors: Optional[str] = None
    warnings: Optional[str] = None
    wrongCells: Optional[List[MatchyWrongCell]] = None

class ProductBase(OurBaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category_id: int

class ProductOut(ProductBase):
    id: int
    image_link:str
    created_at: datetime

class ProductsOut(PagedResponse):
    list: List[ProductOut]

class CategoryBase(OurBaseModel):
    name: str
    description: str

class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    image_link: str

class CategoriesOut(PagedResponse):
    list: List[CategoryOut]

class PricelistBase(OurBaseModel):
    name: str
    description: str

class PricelistOut(PricelistBase):
    id: int
    created_at: datetime

class PricelistsOut(PagedResponse):
    list: List[PricelistOut]

class PricelistLineBase(OurBaseModel):
    new_price: float
    min_quantity: int
    start_date: datetime
    end_date: datetime
    pricelist_id: int
    product_id: int

class PricelistLineOut(PricelistLineBase):
    id: int
    pricelist: PricelistOut
    product: ProductOut

class ProgramBase(OurBaseModel):
    name: str
    description: str
    program_type: ProgramType 
    start_date: datetime
    end_date: datetime
    discount: Optional[float] = None
    product_to_buy_id: Optional[int] = None
    product_to_get_id: Optional[int] = None

class ProgramCreate(ProgramBase):
    items_count:Optional[int]

class ProgramUpdate(ProgramBase):
    pass

class ProgramOut(ProgramBase):
    id: int 

class ProgramsOut(PagedResponse):
    list:List[ProgramOut]

class ProgramItemBase(OurBaseModel):
    code:str
    program_id:int
    status:ProgramItemType

class ProgramItemOut(ProgramItemBase):
    id:int

class ProgramItemsOut(PagedResponse):
    list:List[ProgramItemOut]