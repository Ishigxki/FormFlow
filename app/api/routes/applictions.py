from fastapi import APIRouter, Depends, HTTPException
from app.schemas.Applications import ApplicationCreate, ApplicationResponse, ApplicationUpdate,MessageResponse,ApplicationListResponse
from app.api.routes.dependencies import get_db
from app.enums.application_status import ApplicationStatus
from app.models.Applications import Applications
from sqlalchemy.orm import joinedload

from app.models.student_profile import StudentProfile

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.security.student_dependencies import get_current_student_profile
from app.security.application_dependencies import get_student_application
from app.models.Opportunities import Opportunity



router = APIRouter()

@router.post("/applications", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db),student_profile: StudentProfile = Depends(get_current_student_profile)):

    #student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()

    opportunity = db.get(Opportunity, application.opportunity_id)

    if opportunity is None:
        raise HTTPException(status_code=404,detail="Opportunity not found")

    existing_application =db.query(Applications).filter(Applications.opportunity_id == application.opportunity_id,Applications.student_id == student_profile.id).first()
    if existing_application:
        raise HTTPException(status_code=400,detail="Student has already applied to this opportunity")

    new_application = Applications(
    student_id=student_profile.id,
    opportunity_id=application.opportunity_id,
    status=ApplicationStatus.PENDING.value,
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc)
)
   
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    new_application = (
    db.query(Applications).options(joinedload(Applications.opportunity)).filter(Applications.id == new_application.id).first())
    return new_application

@router.get("/applications",response_model=ApplicationListResponse)
def get_applications(page: int = 1,limit: int = 10,db: Session = Depends(get_db),student_profile: StudentProfile = Depends(get_current_student_profile)):
    #student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    total = (db.query(Applications).filter(Applications.student_id == student_profile.id).count())

    offset = (page - 1) * limit

    total_pages = (total + limit - 1) // limit


    applications = (db.query(Applications).options(joinedload(Applications.opportunity)).filter(Applications.student_id == student_profile.id).offset(offset).limit(limit).all())
    return {"total": total,"page": page,"limit": limit,"total_pages": total_pages,"items": applications,}

@router.get("/applications/{application_id}",response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db),student_profile: StudentProfile = Depends(get_current_student_profile)):
    #student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    
    application = get_student_application(application_id,student_profile,db,)


    

    return application
    



@router.delete("/applications/{application_id}",response_model=MessageResponse)
def delete_application(application_id:int,db : Session = Depends(get_db),student_profile: StudentProfile = Depends(get_current_student_profile)):
    #student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        
    application_to_delete =get_student_application(application_id,student_profile,db,)

    
    db.delete(application_to_delete)
    db.commit()

    return {
    "message": f"Application {application_id} deleted successfully"
}