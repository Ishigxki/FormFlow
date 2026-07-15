from fastapi import APIRouter
from app.schemas.opptunities import OpportunityCreate
from app.api.routes.dependencies import get_db
from app.models.Opportunities import Opportunity
from sqlalchemy.orm import Session
from fastapi import Depends


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