from app.database import Base
from sqlalchemy import Column,Integer,Float,String,ForeignKey,DateTime,func
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__="orders"
    id=Column(Integer,nullable=False,primary_key=True)
    number=Column(String,nullable=False)
    total_price=Column(Float,nullable=False)
    customer_id=Column(Integer,ForeignKey("customers.id"),nullable=True)
    session_id=Column(Integer,ForeignKey("sessions.id"),nullable=False)
    pricelist_id=Column(Integer,ForeignKey("pricelists.id"),nullable=True)
    program_item_id=Column(Integer,ForeignKey("program_items.id"),nullable=True)
    created_at=Column(DateTime,server_default=func.now())
    session =relationship("Session")
    
