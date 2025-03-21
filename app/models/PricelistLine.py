from app.database import Base
from sqlalchemy import Column, Date, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship


class PricelistLine(Base):
    __tablename__ = "pricelist_lines"
    id = Column(Integer, nullable=False, primary_key=True)
    new_price = Column(Float, nullable=False)
    min_quantity = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    pricelist_id = Column(Integer, ForeignKey("pricelists.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product = relationship("Product")
    __table_args__ = (CheckConstraint("start_date < end_date"),)
