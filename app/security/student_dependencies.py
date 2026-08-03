from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.routes.dependencies import get_db
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.security.dependencies import get_current_user


def get_current_student_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StudentProfile:

    student_profile = (db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first())

    if student_profile is None:
        raise HTTPException(status_code=404,detail="Student profile not found",)

    return student_profile