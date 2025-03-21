from app.database import Base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.enums import ProgramItemType
from sqlalchemy.orm import relationship


class ProgramItem(Base):
    __tablename__ = "program_items"
    id = Column(Integer, nullable=False, primary_key=True)
    code = Column(String, nullable=False)
    status = Column(Enum(ProgramItemType), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id", ondelete="CASCADE"))
    program=relationship("Program",back_populates="items")
    order_id = Column(Integer,ForeignKey('orders.id'),nullable=True)
