from app.database import Base
from app.enums import ProgramType
from sqlalchemy import Column, Date ,Integer,Float,String,Enum,ForeignKey,CheckConstraint
from sqlalchemy.orm import relationship


class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    program_type = Column(Enum(ProgramType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    discount = Column(Float, nullable=True)
    product_to_buy_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=True)
    product_to_get_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=True)
    items=relationship("ProgramItem",back_populates="program")
    product_to_buy=relationship("Product",foreign_keys=[product_to_buy_id])
    product_to_get=relationship("Product",foreign_keys=[product_to_get_id])
    __table_args__ = (
        CheckConstraint("start_date < end_date", name="valid_program_date"),
        CheckConstraint("((program_type = 'Coupon' AND discount IS NOT NULL AND product_to_buy_id IS NULL AND product_to_get_id IS NULL) OR (program_type = 'BuyXgetY' AND discount IS NULL AND product_to_buy_id IS NOT NULL AND product_to_get_id IS NOT NULL))",name="program_type_constraints"),
    )
