from fastapi import APIRouter
from app.schemas.Applications import ApplicationCreate  
from app.api.routes.dependencies import get_db
from app.models.Applications import Applications
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException


router = APIRouter()

@router.post("/applications")
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    new_application = Applications(
        id=application.id,
        student_id=application.student_id,
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
def get_applications(db: Session = Depends(get_db)):
    applications = db.query(Applications).all()
    return applications

@router.get("/applications/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Applications).filter(Applications.id == application_id).first()
    if application is None:
        return {"error": "Application not found"}
    return {
        "id": application.id,
        "student_id": application.student_id,
        "opportunity_id": application.opportunity_id,
        "status": application.status,
        "created_at": application.created_at,
        "updated_at": application.updated_at
    }

@router.put("/applications/{application_id}")
def application_update(application_id:int,application:ApplicationCreate, db: Session =Depends(get_db)):
    application_to_update = db.query(Applications).filter(Applications.id == application_id).first()
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