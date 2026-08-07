from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False, unique=True)

    website = Column(String(255), nullable=True)

    description = Column(String(500), nullable=True)

    logo_url = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)

    is_deleted = Column(Boolean, default=False, nullable=False)

    deleted_at = Column(DateTime(timezone=True), nullable=True)

    opportunities = relationship(
        "Opportunity",
        back_populates="company"
    )