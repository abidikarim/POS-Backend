from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

class Pricelist(Base):
    __tablename__ = "pricelists"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    pricelist_lines=relationship("PricelistLine")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
