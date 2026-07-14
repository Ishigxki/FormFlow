from pydantic import BaseModel, EmailStr




class UserCreate(BaseModel):
    password: str
    email: EmailStr
    username: str
    