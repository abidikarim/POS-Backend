from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func, Float
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_link = Column(String, nullable=False)
    public_id=Column(String,nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
