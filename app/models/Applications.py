from sqlalchemy import Column, Integer, String, Datetime,ForeignKey

from app.database.database import Base


class Applications(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id =Column(Integer, ForeignKey("student_profile.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    status = Column(String(20),nullable=False)
    created_at = Column(Datetime, nullable=False)
    updated_at = Column(Datetime, nullable=False)

