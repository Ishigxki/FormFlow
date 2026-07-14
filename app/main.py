from fastapi import FastAPI
from app.api.routes import users

app = FastAPI()
app.include_router(users.router)
@app.get("/")

def home():
    return {
        "message": "Welcome to formflow API"
    }