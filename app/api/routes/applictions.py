from fastapi import APIRouter, Depends, HTTPException
from app.schemas.Applications import ApplicationCreate, ApplicationResponse, ApplicationUpdate,MessageResponse
from app.api.routes.dependencies import get_db
from app.models.Applications import Applications
from app.security.dependencies import get_current_user
from app.models.student_profile import StudentProfile
from app.models.user import User
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone



router = APIRouter()

@router.post("/applications", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):

    student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if student_profile is None:
        raise HTTPException(status_code=404,detail="Student profile not found")

    existing_application =db.query(Applications).filter(Applications.opportunity_id == application.opportunity_id,Applications.student_id == student_profile.id).first()
    if existing_application:
        raise HTTPException(status_code=400,detail="Student has already applied to this opportunity")

    new_application = Applications(
    student_id=student_profile.id,
    opportunity_id=application.opportunity_id,
    status="Pending",
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc)
)
   
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application

@router.get("/applications",response_model=List[ApplicationResponse])
def get_applications(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()

    if student_profile is None:
        raise HTTPException(status_code=404,detail="Student profile not found")

    applications = db.query(Applications).filter(Applications.student_id == student_profile.id).all()

    return applications

@router.get("/applications/{application_id}",response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    if student_profile is None:
        raise HTTPException(status_code=404,detail="Student profile not found")
    
    application =db.query(Applications).filter(Applications.id == application_id,Applications.student_id == student_profile.id).first()

    if application is None:
        raise HTTPException(
    status_code=404,
    detail="Application not found"
)
    

    return application
    

@router.put("/applications/{application_id}",response_model=ApplicationResponse)
def application_update(application_id:int,application:ApplicationUpdate, db: Session =Depends(get_db),current_user: User = Depends(get_current_user)):
    student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        
    if student_profile is None:
        raise HTTPException(status_code=404,detail="Student profile not found")
        
    application_to_update = db.query(Applications).filter(Applications.id == application_id,Applications.student_id == student_profile.id).first()
    
    if application_to_update is None:
        raise HTTPException(status_code=404, detail="Application Not Found")
    
    application_to_update.status = application.status
    application_to_update.updated_at = datetime.now(timezone.utc)


    db.commit()
    db.refresh(application_to_update)


    return application_to_update

@router.delete("/applications/{application_id}",response_model=MessageResponse)
def delete_application(application_id:int,db : Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        
    if student_profile is None:
        raise HTTPException(status_code=404,detail="Student profile not found")
        
    application_to_delete =db.query(Applications).filter(Applications.id == application_id,Applications.student_id == student_profile.id).first()

    if application_to_delete is None:
        raise HTTPException (status_code=404,detail="application not found")
    db.delete(application_to_delete)
    db.commit()

    return {
    "message": f"Application {application_id} deleted successfully"
}