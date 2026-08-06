from fastapi import FastAPI
from app.api.routes import opportunities, student_profile, users, applictions,companies
from app.database.database import Base, engine
from app.models.Applications import Applications
from app.models.user import User
from app.models.Opportunities import Opportunity
from app.models.student_profile import StudentProfile   


#if table does not exist, create it


app = FastAPI()
app.include_router(users.router)
app.include_router(applictions.router)
app.include_router(opportunities.router)
app.include_router(student_profile.router) 
app.include_router(companies.router)
@app.get("/")

def home():
    return {
        "message": "Welcome to formflow API"
    }