from pydantic import BaseModel, Field
from datetime import datetime
from app.enums.application_status import ApplicationStatus
from app.schemas.opptunities import OpportunityResponse
from typing import List

class ApplicationCreate(BaseModel):
    
    opportunity_id: int

class OpportunitySummary(BaseModel):
    id: int
    title: str
    company: str
    deadline: datetime | None
    application_link: str

    model_config = {"from_attributes": True}
    
class ApplicationListResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[ApplicationResponse]

class ApplicationResponse(BaseModel):
    id: int
    student_id: int
    opportunity_id: int
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime

    opportunity: OpportunitySummary

    model_config = {
        "from_attributes": True
    }

class ApplicationUpdate(BaseModel):
    status: ApplicationStatus


class MessageResponse(BaseModel):
    message: str

