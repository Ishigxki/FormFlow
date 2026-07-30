from pydantic import BaseModel
from datetime import datetime

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

class MessageResponse(BaseModel):
    message: str