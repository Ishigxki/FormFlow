from fastapi import APIRouter, Depends, HTTPException
from app.schemas.Applications import ApplicationCreate  
from app.api.routes.dependencies import get_db
from app.models.Applications import Applications
from app.security.dependencies import get_current_user
from app.models.student_profile import StudentProfile
from app.models.user import User
from sqlalchemy.orm import Session



router = APIRouter()

@router.post("/applications")
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
        status=application.status,
        created_at=application.created_at,
        updated_at=application.updated_at
    )
   
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return {
        "id": new_application.id,
        "student_id": new_application.student_id,
        "opportunity_id": new_application.opportunity_id,
        "status": new_application.status,
        "created_at": new_application.created_at,
        "updated_at": new_application.updated_at
    }

@router.get("/applications")
def get_applications(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()

    if student_profile is None:
        raise HTTPException(status_code=404,detail="Student profile not found")

    applications = db.query(Applications).filter(Applications.student_id == student_profile.id).all()

    return applications

@router.get("/applications/{application_id}")
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
    return {
        "id": application.id,
        "student_id": application.student_id,
        "opportunity_id": application.opportunity_id,
        "status": application.status,
        "created_at": application.created_at,
        "updated_at": application.updated_at
    }

@router.put("/applications/{application_id}")
def application_update(application_id:int,application:ApplicationCreate, db: Session =Depends(get_db),current_user: User = Depends(get_current_user)):
    student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        
    if student_profile is None:
        raise HTTPException(status_code=404,detail="Student profile not found")
        
    application_to_update = db.query(Applications).filter(Applications.id == application_id,Applications.student_id == student_profile.id).first()
    
    if application_to_update is None:
        raise HTTPException(status_code=404, detail="Application Not Found")
    
    application_to_update.status = application.status
    application_to_update.updated_at= application.updated_at


    db.commit()
    db.refresh(application_to_update)


    return {
        "id": application_to_update.id,
        "status": application_to_update.status,
        "updated_at":application_to_update.updated_at

    }

@router.delete("/applications/{application_id}")
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