from pydantic import BaseModel, EmailStr
from datetime import datetime

class OpportunityCreate(BaseModel):
    id: int
    title: str
    description: str
    company: str
    type: str
    deadline: datetime
    application_link: str