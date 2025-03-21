from app.database import Base
from sqlalchemy import Column,Integer,Float,ForeignKey

class OrderLine(Base):
    __tablename__="order_lines"
    id=Column(Integer,nullable=False,primary_key=True)
    unit_price=Column(Float,nullable=False)
    total_price=Column(Float,nullable=False)
    quantity=Column(Integer,nullable=False)
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False)
    order_id=Column(Integer,ForeignKey("orders.id"),nullable=False)
