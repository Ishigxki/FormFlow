from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate
from app.api.routes.dependencies import get_db
from app.models.user import User
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/users")
def create_users(user: UserCreate, db: Session = Depends(get_db)):
       

    existing_user = db.query(User).filter(User.email == user.email).first()
    existing_username = db.query(User).filter(User.username == user.username).first()

    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email,username=user.username,password_hash=user.password)

    
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

@router.delete("/users/{user_id}")
def delete_user(user_id: int,db: Session = Depends(get_db)):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="user not found")
    
    db.delete(user_to_delete)
    db.commit()
    
    return {
        "message": f"User {user_id} deleted successfully"
    }

    
