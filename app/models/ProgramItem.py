from app.database import Base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.enums import ProgramItemType


class ProgramItem(Base):
    __tablename__ = "program_items"
    id = Column(Integer, nullable=False, primary_key=True)
    code = Column(String, nullable=False)
    status = Column(Enum(ProgramItemType), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id", ondelete="CASCADE"))

    # Fix that when create orders table
    # order_id = Column(Integer,ForeignKey('orders.id',ondelete="CASCADE"),nullable=True)
