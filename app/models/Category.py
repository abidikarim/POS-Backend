from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from app.database import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_link = Column(String, nullable=False)
    public_id=Column(String,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
