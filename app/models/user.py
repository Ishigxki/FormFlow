from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime
from app.database.database import Base
from datetime import datetime,timezone


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime,nullable =False,default=datetime.utcnow)
    role = Column(String(100),nullable=False, default="student")

    student_profile = relationship("StudentProfile",back_populates="user",uselist=False,cascade="all, delete-orphan")
    

