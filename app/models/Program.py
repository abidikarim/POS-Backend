from app.database import Base
from app.enums import ProgramType
from sqlalchemy import Column ,Integer,Float,String,Enum,DateTime,ForeignKey,CheckConstraint


class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    program_type = Column(Enum(ProgramType), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    discount = Column(Float, nullable=True)
    product_to_buy_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=True)
    product_to_get_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=True)
    __table_args__ = (
        CheckConstraint("start_date < end_date", name="valid_program_date"),
        CheckConstraint("((program_type = 'Coupon' AND discount IS NOT NULL AND product_to_buy_id IS NULL AND product_to_get_id IS NULL) OR (program_type = 'BuyXgetY' AND discount IS NULL AND product_to_buy_id IS NOT NULL AND product_to_get_id IS NOT NULL))",name="program_type_constraints"),
    )
