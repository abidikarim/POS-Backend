import os
from pathlib import Path
from typing import List
from fastapi import APIRouter
from fastapi.responses import FileResponse
from app import schemas
from app.dependencies import dbDep, currentEmployee
from app.enums.emailTemplate import EmailTemplate
from app.services import program,program_item,customer
from app.services.error import  get_error_detail
from app.utilities import send_mail
import tempfile
from jinja2 import Environment, FileSystemLoader
import pdfkit


TEMPLATES_DIR = Path(__file__).parent / "../templates"
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


error_keys={
    "programs_product_to_buy_id_fkey":{"message":"Product to buy not found","status":404},
    "programs_product_to_get_id_fkey":{"message":"Product to get not found","status":404},
    "valid_program_date":{"message":"start_date must be before end_date"},
    "program_type_constraints":{"message":"Set discount with no products. Or set product_to_buy and product_to_get_id with no discount.","status":400},
    "programs_pkey":{"message":"Program not found","status":404}
}

router = APIRouter(prefix="/program",tags=["Program"])

@router.get("",response_model=List[schemas.ProgramOut])
def get_programs(db:dbDep,cur_emp:currentEmployee):
    try:
        data = program.get(db)
        return data
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])

@router.post("")
def create_program(program_data:schemas.ProgramCreate,db:dbDep,cur_emp:currentEmployee):
    try:
        new_program = program.add(program_data.model_dump(),db)
    except Exception as error:
        error_detail = get_error_detail(str(error),error_keys)
        return schemas.BaseOut(status_code=error_detail["status"],detail=error_detail["message"])
    return schemas.BaseOut(status_code=201,detail="Program created")


@router.post("/sendGiftCard")
async def send_gift_card(db:dbDep,data:schemas.GiftCard,cur_emp:currentEmployee):
    try:
        custmr = customer.get_by_id(db,data.customer_id)
        item = program_item.get_by_id(data.code_id,db)
        await send_mail(
            schemas.MailData(
                emails=[custmr.email],
                body={"name": f"{custmr.name}","code":item.code,"discount":item.program.discount,"end_date":item.program.end_date},
                template=EmailTemplate.GiftCardTemplate,
                subject="🎁 Your Gift Card",
            )
        )
        return schemas.BaseOut(status_code=200,detail="Code send successfully")
    except Exception as error:
        error_detail =get_error_detail(str(error),error_keys) 
        return schemas.BaseOut(status_code=error_detail['status'],detail=error_detail['message'])
    
@router.get("/generate-pdf/{item_id}")
def generate_pdf(db:dbDep,item_id:int,cur_emp:currentEmployee):
    try:
        item = program_item.get_by_id(item_id, db)

        if not item:
            return schemas.BaseOut(status_code=404,detail="Code not found")
        data = {
            "code": item.code,
            "discount": item.program.discount,
            "end_date": item.program.end_date,
        }

        # Load and render the HTML template
        template = env.get_template("gift_card.html")  # Load from templates folder
        rendered_html = template.render(data)

        # Generate a temporary PDF file
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, "giftcard.pdf")

        # Convert HTML to PDF using pdfkit
        PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
        pdfkit.from_string(rendered_html, pdf_path, configuration=PDFKIT_CONFIG)
        # Return the PDF file as a response
        return FileResponse(pdf_path, media_type="application/pdf", filename="giftcard.pdf")
    except Exception as error :
        return schemas.BaseOut(status_code=500,detail=str(error))
       
