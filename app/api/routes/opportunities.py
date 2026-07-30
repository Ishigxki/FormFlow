from fastapi import APIRouter, Depends, HTTPException
from app.schemas.opptunities import OpportunityCreate,OpportunityResponse,OpportunityUpdate,MessageResponse
from app.api.routes.dependencies import get_db
from app.models.Opportunities import Opportunity
from sqlalchemy.orm import Session
from app.models.user import User
from app.security.dependencies import get_current_user
from typing import List



router = APIRouter()

@router.post("/opportunities",response_model=OpportunityResponse)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_opportunity = (db.query(Opportunity).filter(Opportunity.title == opportunity.title,Opportunity.company == opportunity.company).first()
)

    if existing_opportunity:
        raise HTTPException(status_code=400,detail="Opportunity already registered")

    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Admin access required")

    new_opportunity = Opportunity(
        title=opportunity.title,
        description=opportunity.description,
        company=opportunity.company,
        type=opportunity.type,
        deadline=opportunity.deadline,
        application_link=opportunity.application_link
    )

    db.add(new_opportunity)
    db.commit()
    db.refresh(new_opportunity)
    return new_opportunity


@router.get("/opportunities",response_model=List[OpportunityResponse])
def get_opportunities(db: Session = Depends(get_db)):
    opportunities = db.query(Opportunity).all()
    return opportunities

@router.get("/opportunities/{opportunity_id}",response_model=OpportunityResponse)  
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if opportunity is None:
       raise HTTPException(status_code=404, detail="Opportunity doesn't exist")
    return opportunity

@router.put("/opportunities/{opportunity_id}",response_model=OpportunityResponse)

def update_opportunities(opportunity_id: int,opportunity:OpportunityUpdate,db:Session =Depends(get_db), current_user: User = Depends(get_current_user)):
    opportunity_to_update = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if opportunity_to_update is None:
        raise HTTPException(status_code=404, detail="Opportunity doesn't exist")
    if current_user.role != "admin":
            raise HTTPException(status_code=403,detail="Admin access required")
    
    opportunity_to_update.title = opportunity.title
    opportunity_to_update.description =opportunity.description
    opportunity_to_update.type = opportunity.type
    opportunity_to_update.deadline = opportunity.deadline
    opportunity_to_update.application_link =opportunity.application_link
    opportunity_to_update.company =opportunity.company

    db.commit()
    db.refresh(opportunity_to_update)

    return opportunity_to_update

@router.delete("/opportunities/{opportunity_id}",response_model=MessageResponse)
def delete_opportunities(opportunity_id: int,db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    opportunity_to_delete = db.query(Opportunity).filter(Opportunity.id==opportunity_id).first()
    if opportunity_to_delete is None:
        raise HTTPException(status_code=404, detail="opportunity not found")
    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Admin access required")
    
    db.delete(opportunity_to_delete)
    db.commit()

    return {
        "message":f"opportunity {opportunity_id} deleted"
    }