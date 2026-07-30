from pydantic import BaseModel, EmailStr



class StudentProfileCreate(BaseModel):
   
    
    first_name: str
    last_name: str
    university: str
    degree: str
    graduation_year: int
    bio: str | None = None
    

class StudentProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    university: str
    degree:str
    graduation_year: int
    bio:str | None = None

    model_config = {
        "from_attributes": True
    }

class MessageResponse(BaseModel):
    message: str