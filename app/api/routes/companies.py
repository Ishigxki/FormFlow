from fastapi import APIRouter, Depends, HTTPException
from app.schemas.company import CompanyCreate,CompanyResponse,CompanySummary,CompanyListResponse,CompanyUpdate,MessageResponse
from app.api.routes.dependencies import get_db
from sqlalchemy.orm import joinedload
from app.models.Company import Company
from fastapi import Query
from typing import List, Optional
from sqlalchemy.orm import Session
import math
from sqlalchemy import or_
from app.models.user import User
from app.security.dependencies import get_current_user



router = APIRouter()

@router.post("/companies",response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Admin access required")
        
    existing_company = (db.query(Company).filter(Company.name ==company.name).first())

    if existing_company:
        raise HTTPException(status_code=400,detail="Company already registered")
   
    
    new_company = Company(
        name = company.name,
        website = company.website,
        description = company.description,
        logo_url = company.logo_url
           
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

@router.get("/companies",response_model=CompanyListResponse)

def get_companies(page: int = Query(1, ge=1),limit:int =Query(10, ge=1, le=100),db: Session =Depends(get_db),search: Optional[str] = None,sort_by:str =Query("id"),order: str =Query("asc")):
    offset = (page -1) *limit
    query = (db.query(Company))

    if search:
        query =query.filter(or_(
            Company.name.ilike(f"%{search}%"),
            Company.description.ilike(f"%{search}%")                             
        )
    )

    allowed_sort_field ={"id": Company.id,"name":Company.name,"description":Company.description,"created_at": Company.created_at}

    sort_column = allowed_sort_field.get(sort_by)


    if sort_column is None:
        raise HTTPException(status_code=400,detail="Invalid sort field")

    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    total = query.count()
    total_pages = math.ceil(total / limit)

    query = query.offset(offset).limit(limit)

    companies = query.all()

    return {"total": total,"page": page,"limit": limit,"total_pages": total_pages,"items": companies}


@router.get("/companies/{company_id}",response_model=CompanyResponse)
def get_company(company_id: int,db: Session =Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company doesn't exist")
    return company


@router.put("/companies/{company_id}",response_model=CompanyResponse)
def update_company(company_id: int, company:CompanyUpdate,db:Session =Depends(get_db),current_user: User =Depends(get_current_user)):
    company_to_update = (db.query(Company).filter(Company.id == company_id).first())

    if company_to_update is None:
        raise HTTPException(status_code=404,detail="Company doesn't exist")

    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Admin access required")

    existing_company = (db.query(Company).filter(Company.name == company.name,Company.id != company_id).first())

    if existing_company:
        raise HTTPException(status_code=400,detail="Company name already exists")

    company_to_update.name =company.name
    company_to_update.description = company.description
    company_to_update.logo_url = company.logo_url
    company_to_update.website =company.website

    db.commit()
    db.refresh(company_to_update)

    return company_to_update


@router.delete("/companies/{company_id}",response_model=MessageResponse)
def delete_companies(company_id: int, db: Session=Depends(get_db), current_user: User =Depends(get_current_user)):
    company_to_delete = db.query(Company).filter(Company.id == company_id).first()
    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Admin access required")

    if company_to_delete is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(company_to_delete)
    db.commit()

    return {
        "message":f"Company {company_id} deleted"
    }