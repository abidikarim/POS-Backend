from app.database import Base
from sqlalchemy import Column,Integer,DateTime,ForeignKey,Enum
from sqlalchemy.orm import relationship
from app.enums import SessionStatus

class Session(Base):
    __tablename__="sessions"
    id=Column(Integer,nullable=False,primary_key=True)
    opened_at=Column(DateTime,nullable=False)
    closed_at=Column(DateTime,nullable=True)
    status=Column(Enum(SessionStatus),nullable=False,default=SessionStatus.Open)
    employee_id=Column(Integer,ForeignKey("employees.id"),nullable=False)
    employee=relationship("Employee",foreign_keys=[employee_id])