from fastapi import APIRouter
from app.schemas.opptunities import OpportunityCreate
from app.api.routes.dependencies import get_db
from app.models.Opportunities import Opportunity
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException


router = APIRouter()

@router.post("/opportunities")
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    new_opportunity = Opportunity(
        id=opportunity.id,
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
    return {
        "id": new_opportunity.id,
        "title": new_opportunity.title,
        "description": new_opportunity.description,
        "company": new_opportunity.company,
        "type": new_opportunity.type,
        "deadline": new_opportunity.deadline,
        "application_link": new_opportunity.application_link
    }


@router.get("/opportunities")
def get_opportunities(db: Session = Depends(get_db)):
    opportunities = db.query(Opportunity).all()
    return opportunities

@router.get("/opportunities/{opportunity_id}")  
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if opportunity is None:
        return {"error": "Opportunity not found"}
    return {
        "id": opportunity.id,
        "title": opportunity.title,
        "description": opportunity.description,
        "company": opportunity.company,
        "type": opportunity.type,
        "deadline": opportunity.deadline,
        "application_link": opportunity.application_link
    }

@router.put("/opportunities/{opportunity_id}")

def update_opportunities(opportunity_id: int,opportunity:OpportunityCreate,db:Session =Depends(get_db)):
    opportunity_to_update = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if opportunity_to_update is None:
        raise HTTPException(status_code=404, detail="Opportunity doesn't exist")
    
    opportunity_to_update.title = opportunity.title
    opportunity_to_update.description =opportunity.description
    opportunity_to_update.type = opportunity.type
    opportunity_to_update.deadline = opportunity.deadline
    opportunity_to_update.application_link =opportunity.application_link
    opportunity_to_update.company =opportunity.company

    db.commit()
    db.refresh(opportunity_to_update)

    return {
        "id" :opportunity_to_update.id,
        "title": opportunity_to_update.title,
        "description":opportunity_to_update.description,
        "type":opportunity_to_update.type,
        "deadline":opportunity_to_update.deadline,
        "application_link":opportunity_to_update.application_link,
        "company":opportunity_to_update.company
    }

@router.delete("/opportunities/{opportunity_id}")
def delete_opportunities(opportunity_id: int,db: Session=Depends(get_db)):
    opportunity_to_delete = db.query(Opportunity).filter(Opportunity.id==opportunity_id).first()
    if opportunity_to_delete is None:
        raise HTTPException(status_code=404, detail="opportunity not found")
    
    db.delete(opportunity_to_delete)
    db.commit()

    return {
        "message":f"opportunity {opportunity_id} deleted"
    }