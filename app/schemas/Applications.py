from pydantic import BaseModel, Field
from datetime import datetime

class ApplicationCreate(BaseModel):
    
    opportunity_id: int
    
    