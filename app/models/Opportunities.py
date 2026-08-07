from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship






class Opportunity(Base):
    __tablename__ = "opportunities"

   
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    type = Column(String(100), nullable=False)
    deadline = Column(DateTime)
    application_link = Column(String(255), nullable=False)

    company = relationship("Company",back_populates="opportunities")
    applications = relationship("Applications",back_populates="opportunity")
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
