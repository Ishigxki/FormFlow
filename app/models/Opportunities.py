from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

def utc_now():
    return datetime.now(timezone.utc)



class Opportunity(Base):
    __tablename__ = "opportunities"

   
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    deadline = Column(DateTime)
    application_link = Column(String(255), nullable=False)

    applications = relationship("Applications",back_populates="opportunity")
    
