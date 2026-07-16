from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.api.routes.dependencies import get_db
from app.models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import Depends

router = APIRouter()


@router.post("/users")
def create_users(user: UserCreate, db: Session = Depends(get_db)):
       

    new_user = User(
        email=user.email,
        username=user.username,
        password_hash=user.password
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }
        
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    
@router.put("/users/{user_id}")
def update_user(user_id: int,user:UserCreate, db: Session = Depends(get_db)):
    user_to_update = db.query(User).filter(User.id == user_id).first()
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_to_update.username = user.username
    user_to_update.email =user.email
    user_to_update.password_hash = user.password


    db.commit()
    db.refresh(user_to_update)

    return {
        "id": user_to_update.id,
        "username": user_to_update.username,
        "email": user_to_update.email
    }


    
