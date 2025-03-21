from app.database import Base
from sqlalchemy import Column,String,Integer,TIMESTAMP,DATE,Enum,func,CheckConstraint,ForeignKey

class Customer(Base):
    __tablename__="customers"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False)
    pricelist_id =Column(Integer,ForeignKey("pricelists.id"),nullable=True)