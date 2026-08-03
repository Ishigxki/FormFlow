from fastapi import APIRouter, Depends, HTTPException
from app.schemas.Applications import ApplicationCreate, ApplicationResponse, ApplicationUpdate,MessageResponse,ApplicationListResponse
from app.api.routes.dependencies import get_db
from sqlalchemy import or_
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
def get_applications(page: int = 1,limit: int = 10,status: ApplicationStatus | None = None,search: str | None = None,sort_by: str = "created_at",order: str = "desc",db: Session = Depends(get_db),student_profile: StudentProfile = Depends(get_current_student_profile)):
    #student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    offset = (page - 1) * limit
    query = (db.query(Applications).join(Opportunity).options(joinedload(Applications.opportunity)).filter(Applications.student_id == student_profile.id))
    
    if status is not None:
        query = query.filter(Applications.status == status.value)

    if search:
        query = query.filter(or_(Opportunity.title.ilike(f"%{search}%"),Opportunity.company.ilike(f"%{search}%"),))

    sort_columns = {"created_at": Applications.created_at,"updated_at": Applications.updated_at,"status": Applications.status,}
    if sort_by not in sort_columns:
        raise HTTPException(status_code=400,detail="Invalid sort field.")
    column = sort_columns[sort_by]

    if order.lower() not in ("asc", "desc"):
        raise HTTPException(status_code=400,detail="Invalid sort order.")

    if order.lower() == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    
    total = query.count()
    total_pages = (total + limit - 1) // limit


    applications = (query.offset(offset).limit(limit).all())
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