from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

def utc_now():
    return datetime.now(timezone.utc)


class StudentProfile(Base):
    __tablename__ = "student_profile"

    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    university = Column(String(100), nullable=False)
    degree = Column(String(100), nullable=False)
    graduation_year = Column(Integer, nullable=False)
    bio = Column(String(255), nullable=True)


    user =relationship("User", back_populates="student_profile")
    applications = relationship("Applications",back_populates="student",cascade="all, delete-orphan")
    
    
