from sqlalchemy.orm import Session,joinedload
from app import models,schemas
from app.dependencies import OrderFilter
from sqlalchemy import func

from app.services.employee import convert_employee_to_schema
from app.utilities import div_ciel

def get(db:Session,pg_params:OrderFilter):
    skip = pg_params.limit * (pg_params.page - 1)
    query = db.query(models.Order).options(joinedload(models.Order.session)).join(models.Session).join(models.Employee)
    if pg_params.name:
        query = query.filter(func.lower(func.concat(models.Employee.first_name+" "+models.Employee.last_name)).contains(func.lower(pg_params.name)))
    if pg_params.session_id:
        query = query.filter(models.Session.id == pg_params.session_id)
    if pg_params.ref:
        query = query.filter(models.Order.id == pg_params.ref)
    if pg_params.number:
        query = query.filter(func.lower(models.Order.number).contains(func.lower(pg_params.number)))
    total_records= query.count()
    total_pages= div_ciel(total_records,pg_params.limit)
    result = query.limit(pg_params.limit).offset(skip).all()
    return schemas.OrdersOut(
        list=[schemas.OrderOut(
            id=order.id,
            number=order.number,
            total_price=order.total_price,
            customer_id=order.customer_id,
            session_id=order.session_id,
            pricelist_id=order.pricelist_id,
            program_item_id=order.program_item_id,
            created_at=order.created_at,
            session=schemas.SessionOut(
                id=order.session.id,
                opened_at=order.session.opened_at,
                closed_at=order.session.closed_at,
                employee_id=order.session.employee_id,
                status=order.session.status,
                employee=convert_employee_to_schema(order.session.employee)
            )
        )
        for order in result
    ],
        total_pages=total_pages,
        total_records=total_records,
        page_size=pg_params.limit,
        page_number=pg_params.page,
        status_code=200,
        detail="Orders fetched" 
    )
