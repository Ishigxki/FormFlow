from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.database.database import Base



class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    deadline = Column(DateTime)
    application_link = Column(String(255), nullable=False)
