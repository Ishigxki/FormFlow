from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.Applications import Applications
from sqlalchemy.orm import joinedload
from app.models.student_profile import StudentProfile


def get_student_application(
    application_id: int,
    student_profile: StudentProfile,
    db: Session,
):
    application = (
        db.query(Applications).options(joinedload(Applications.opportunity))
        .filter(
            Applications.id == application_id,
            Applications.student_id == student_profile.id,
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application