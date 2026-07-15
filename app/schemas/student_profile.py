from pydantic import BaseModel, EmailStr



class StudentProfileCreate(BaseModel):
    user_id: int
    
    first_name: str
    last_name: str
    university: str
    degree: str
    graduation_year: int
    bio: str | None = None
    

