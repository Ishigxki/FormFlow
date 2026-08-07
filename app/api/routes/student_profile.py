from fastapi import APIRouter, Depends, HTTPException
from app.schemas.student_profile import StudentProfileCreate,MessageResponse
from app.api.routes.dependencies import get_db
from app.models.user import User
from app.models.student_profile import StudentProfile,utc_now
from app.security.dependencies import get_current_user
from sqlalchemy.orm import Session



router = APIRouter()

@router.post("/student_profile")
def create_student_profile(student_profile: StudentProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    existing_profile = (db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id,StudentProfile.is_deleted == False).first())

    if existing_profile:
        raise HTTPException(status_code=400,
        detail="Student profile already exists"
    )

    
    new_student_profile = StudentProfile(
        user_id=current_user.id,
        first_name = student_profile.first_name,
        last_name = student_profile.last_name,
        university=student_profile.university,
        degree=student_profile.degree,
        graduation_year=student_profile.graduation_year,
        bio=student_profile.bio
    )

    db.add(new_student_profile)
    db.commit()
    db.refresh(new_student_profile)
    return {
    "id": new_student_profile.id,
    "user_id": new_student_profile.user_id,
    "first_name": new_student_profile.first_name,
    "last_name": new_student_profile.last_name,
    "university": new_student_profile.university,
    "degree": new_student_profile.degree,
    "graduation_year": new_student_profile.graduation_year,
    "bio": new_student_profile.bio
}

@router.get("/student_profile")
def get_student_profile(db: Session = Depends(get_db)):
    student_profiles = db.query(StudentProfile).filter(StudentProfile.is_deleted == False).all()
    return student_profiles


@router.get("/student_profile/me")   
def get_student_profile_by_user_id(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    student_profile = (db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id,StudentProfile.is_deleted == False).first())
    if student_profile is None:
        raise HTTPException(status_code=404, detail="student profile not found")
    return {
        "id": student_profile.id,
        "user_id": student_profile.user_id,
        "first_name": student_profile.first_name,
        "last_name": student_profile.last_name,
        "university": student_profile.university,
        "degree": student_profile.degree,
        "graduation_year": student_profile.graduation_year,
        "bio": student_profile.bio
    }

@router.put("/student_profile/me")
def update_student_profile(student_profile: StudentProfileCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    student_to_update = db.query(StudentProfile).filter(StudentProfile.user_id ==current_user.id,StudentProfile.is_deleted == False).first()
    if student_to_update is None:
         raise HTTPException(status_code=404,detail="student profile not found")
    
    
    student_to_update.first_name = student_profile.first_name
    student_to_update.last_name = student_profile.last_name
    student_to_update.university=student_profile.university
    student_to_update.degree=student_profile.degree
    student_to_update.bio=student_profile.bio
    student_to_update.graduation_year=student_profile.graduation_year

    
    db.commit()
    db.refresh(student_to_update)

    return {
        "user_id":student_to_update.user_id,
        "first_name":student_to_update.first_name,
        "last_name":student_to_update.last_name,
        "university":student_to_update.university,
        "degree": student_to_update.degree,
        "graduation_year":student_to_update.graduation_year,
        "bio":student_to_update.bio

    }

@router.delete("/student_profile/me",response_model=MessageResponse)
def delete_student_profile(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    student_profile_to_delete = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id,StudentProfile.is_deleted == False).first()
    if student_profile_to_delete is None:
        raise HTTPException(status_code=404,detail="student profile not found")
    
    student_profile_to_delete.is_deleted = True
    student_profile_to_delete.deleted_at = utc_now()
    db.commit()

    return{
        "message":"Student profile deleted"
    }