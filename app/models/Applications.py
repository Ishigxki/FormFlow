from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from app.enums.application_status import ApplicationStatus
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime,timezone
from sqlalchemy import UniqueConstraint

def utc_now():
        return datetime.now(timezone.utc)

class Applications(Base):
    __tablename__ = "applications"

    __table_args__ = (UniqueConstraint("student_id","opportunity_id",name="uq_student_opportunity"),)

    
    

    id = Column(Integer, primary_key=True, index=True)
    student_id =Column(Integer, ForeignKey("student_profile.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    status = Column(String(20),nullable=False, default=ApplicationStatus.PENDING.value)
    created_at = Column(DateTime, nullable=False, default=utc_now)
    updated_at = Column(DateTime,nullable=False,default=utc_now,onupdate=utc_now)

    student = relationship("StudentProfile",back_populates="applications")
    
    opportunity = relationship("Opportunity", back_populates="applications")
    

