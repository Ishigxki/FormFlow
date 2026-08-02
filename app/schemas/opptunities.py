from pydantic import BaseModel
from datetime import datetime
from typing import List


class OpportunityCreate(BaseModel):
    title: str
    description: str
    company: str
    type: str
    deadline: datetime
    application_link: str


class OpportunityUpdate(BaseModel):
    title: str
    description: str
    company: str
    type: str
    deadline: datetime
    application_link: str


class OpportunityResponse(BaseModel):
    id: int
    title: str
    description: str
    company: str
    type: str
    deadline: datetime
    application_link: str

    model_config = {
        "from_attributes": True
    }


class OpportunityListResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[OpportunityResponse]

class MessageResponse(BaseModel):
    message: str