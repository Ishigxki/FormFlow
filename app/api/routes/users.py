from fastapi import APIRouter
from app.schemas.user import UserCreate

router = APIRouter()


@router.post("/users")
def create_users(user: UserCreate):
    return {
        "Welcome ": user.username,
        "email": user.email
    }