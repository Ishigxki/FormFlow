from fastapi import APIRouter, Depends, HTTPException
from app.schemas.opptunities import OpportunityCreate,OpportunityResponse,OpportunityUpdate,MessageResponse,OpportunityListResponse
from app.api.routes.dependencies import get_db
from app.security.require_admin import require_admin
from app.models.Company import Company,utc_now
from sqlalchemy.orm import joinedload

from fastapi import Query
from app.models.Opportunities import Opportunity
from sqlalchemy.orm import Session
import math
from sqlalchemy import or_
from app.models.user import User

from typing import  Optional



router = APIRouter()

@router.post("/opportunities",response_model=OpportunityResponse)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    existing_opportunity = (db.query(Opportunity).filter(Opportunity.title == opportunity.title,Opportunity.company_id == opportunity.company_id,Opportunity.is_deleted == False).first())

    

    if existing_opportunity:
        raise HTTPException(status_code=400,detail="Opportunity already registered")


    company = (
    db.query(Company)
    .filter(
        Company.id == opportunity.company_id,
        Company.is_deleted == False,
    )
    .first()
)

    if company is None:
        raise HTTPException(status_code=404,detail="Company not found")

    new_opportunity = Opportunity(
        title=opportunity.title,
        description=opportunity.description,
        company_id=opportunity.company_id,
        type=opportunity.type,
        deadline=opportunity.deadline,
        application_link=opportunity.application_link
    )

    db.add(new_opportunity)
    db.commit()
    db.refresh(new_opportunity)
    new_opportunity = (db.query(Opportunity).join(Company).options(joinedload(Opportunity.company)).filter(Opportunity.id == new_opportunity.id,Opportunity.is_deleted == False,Company.is_deleted==False).first())
    return new_opportunity


@router.get("/opportunities",response_model=OpportunityListResponse)
def get_opportunities(page: int = Query(1, ge=1),limit: int = Query(10, ge=1, le=100),db: Session = Depends(get_db),company: Optional[str]=None,opportunity_type: Optional[str] = None,search: Optional[str] = None,sort_by:str =Query("id"),order: str =Query("asc")):
    offset = (page -1) *limit
    query = (db.query(Opportunity).join(Company).options(joinedload(Opportunity.company)).filter(Opportunity.is_deleted == False,Company.is_deleted == False))

    if search:
        query = query.filter(or_(
            Opportunity.title.ilike(f"%{search}%"),
            Opportunity.description.ilike(f"%{search}%"),
            Company.name.ilike(f"%{search}%")
        )
    )

    allowed_sort_fields = {"id": Opportunity.id,"title": Opportunity.title,"company": Company.name,"deadline": Opportunity.deadline,"type": Opportunity.type,}

    sort_column = allowed_sort_fields.get(sort_by)

    if sort_column is None:
        raise HTTPException(status_code=400,detail="Invalid sort field")
   

    if company:
        query = query.filter(Company.name == company)
        
    if opportunity_type:
        query = query.filter(Opportunity.type == opportunity_type)


    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    total = query.count()
    total_pages = math.ceil(total / limit)

    query = query.offset(offset).limit(limit)

    opportunities = query.all()

    
    
    return {"total": total,"page": page,"limit": limit,"total_pages": total_pages,"items": opportunities,}

@router.get("/opportunities/{opportunity_id}",response_model=OpportunityResponse)  
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = (
    db.query(Opportunity)
    .join(Company)
    .options(joinedload(Opportunity.company))
    .filter(
        Opportunity.id == opportunity_id,
        Opportunity.is_deleted == False,
        Company.is_deleted == False,
    )
    .first()
)
    if opportunity is None:
       raise HTTPException(status_code=404, detail="Opportunity doesn't exist")
    return opportunity



@router.put("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunities(
    opportunity_id: int,
    opportunity: OpportunityUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):

    opportunity_to_update = (
        db.query(Opportunity)
        .filter(Opportunity.id == opportunity_id,Opportunity.is_deleted == False)
        .first()
    )

    if opportunity_to_update is None:
        raise HTTPException(
            status_code=404,
            detail="Opportunity doesn't exist"
        )


    company = (
    db.query(Company)
    .filter(
        Company.id == opportunity.company_id,
        Company.is_deleted == False,
    )
    .first()
)

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    opportunity_to_update.title = opportunity.title
    opportunity_to_update.description = opportunity.description
    opportunity_to_update.company_id = opportunity.company_id
    opportunity_to_update.type = opportunity.type
    opportunity_to_update.deadline = opportunity.deadline
    opportunity_to_update.application_link = opportunity.application_link

    db.commit()

    updated = (db.query(Opportunity).join(Company).options(joinedload(Opportunity.company)).filter(Opportunity.id == opportunity_id,Opportunity.is_deleted == False,Company.is_deleted == False).first())

    return updated

@router.delete("/opportunities/{opportunity_id}",response_model=MessageResponse)
def delete_opportunities(opportunity_id: int,db: Session=Depends(get_db), _: User = Depends(require_admin)):
    opportunity_to_delete = (
    db.query(Opportunity)
    .filter(
        Opportunity.id == opportunity_id,
        Opportunity.is_deleted == False,
    )
    .first()
)
    if opportunity_to_delete is None:
        raise HTTPException(status_code=404, detail="opportunity not found")
    
    opportunity_to_delete.is_deleted = True
    opportunity_to_delete.deleted_at = utc_now()
    db.commit()

    return {
        "message":f"opportunity {opportunity_id} deleted"
    }