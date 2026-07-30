from pydantic import BaseModel, Field
from datetime import datetime

class ApplicationCreate(BaseModel):
    
    opportunity_id: int
    


class ApplicationResponse(BaseModel):
    id: int
    student_id: int
    opportunity_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class ApplicationUpdate(BaseModel):
    status: str


class MessageResponse(BaseModel):
    message: str