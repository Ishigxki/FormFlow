from pydantic import BaseModel, Field
from datetime import datetime

class ApplicationCreate(BaseModel):
    id: int
    student_id: int
    opportunity_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    