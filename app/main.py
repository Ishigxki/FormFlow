from fastapi import FastAPI
from app.api.routes import student_profile, users
from app.database.database import Base, engine
from app.models.Applications import Applications
from app.models.user import User
from app.models.Opportunities import Opportunity
from app.models.student_profile import StudentProfile   


#if table does not exist, create it
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(student_profile.router) 
@app.get("/")

def home():
    return {
        "message": "Welcome to formflow API"
    }