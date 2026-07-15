from fastapi import APIRouter
from app.schemas.student_profile import StudentProfileCreate
from app.api.routes.dependencies import get_db
from app.models.student_profile import StudentProfile
from sqlalchemy.orm import Session
from fastapi import Depends


router = APIRouter()

@router.post("/student_profile")
def create_student_profile(student_profile: StudentProfileCreate, db: Session = Depends(get_db)):
    new_student_profile = StudentProfile(
        user_id=student_profile.user_id,
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