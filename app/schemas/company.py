from pydantic import BaseModel
from typing import List


class CompanyCreate(BaseModel):
    name: str
    website: str | None = None
    description: str | None = None
    logo_url: str | None = None

class CompanyUpdate(BaseModel):
    name: str
    website: str | None = None
    description: str | None = None
    logo_url: str | None = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    website: str | None
    description: str | None
    logo_url: str | None

    model_config = {
        "from_attributes": True
    }


class CompanySummary(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class CompanyListResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[CompanyResponse]

class MessageResponse(BaseModel):
    message: str