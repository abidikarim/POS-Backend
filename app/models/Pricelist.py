from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func


class Pricelist(Base):
    __tablename__ = "pricelists"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
