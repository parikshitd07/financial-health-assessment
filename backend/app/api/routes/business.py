"""Business Management Routes"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.models.business import Business, IndustryType, BusinessSize

router = APIRouter()


class BusinessResponse(BaseModel):
    """Business response model"""
    id: int
    business_name: str
    legal_name: Optional[str]
    industry: str
    business_size: str
    gst_number: Optional[str]
    annual_revenue: Optional[float]
    employee_count: Optional[int]
    established_year: Optional[int]
    city: Optional[str]
    state: Optional[str]
    
    class Config:
        from_attributes = True


@router.get("/user/{user_id}", response_model=List[BusinessResponse])
async def get_user_businesses(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all businesses for a specific user"""
    businesses = db.query(Business).filter(
        Business.user_id == user_id
    ).all()
    
    return [
        BusinessResponse(
            id=b.id,
            business_name=b.business_name,
            legal_name=b.legal_name,
            industry=b.industry.value if b.industry else "other",
            business_size=b.business_size.value if b.business_size else "small",
            gst_number=b.gst_number,
            annual_revenue=b.annual_revenue,
            employee_count=b.employee_count,
            established_year=b.established_year,
            city=b.city,
            state=b.state
        )
        for b in businesses
    ]


@router.get("/", response_model=List[BusinessResponse])
async def get_all_businesses(db: Session = Depends(get_db)):
    """Get all businesses (for admin/testing)"""
    businesses = db.query(Business).all()
    
    return [
        BusinessResponse(
            id=b.id,
            business_name=b.business_name,
            legal_name=b.legal_name,
            industry=b.industry.value if b.industry else "other",
            business_size=b.business_size.value if b.business_size else "small",
            gst_number=b.gst_number,
            annual_revenue=b.annual_revenue,
            employee_count=b.employee_count,
            established_year=b.established_year,
            city=b.city,
            state=b.state
        )
        for b in businesses
    ]


@router.get("/{business_id}", response_model=BusinessResponse)
async def get_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific business by ID"""
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    return BusinessResponse(
        id=business.id,
        business_name=business.business_name,
        legal_name=business.legal_name,
        industry=business.industry.value if business.industry else "other",
        business_size=business.business_size.value if business.business_size else "small",
        gst_number=business.gst_number,
        annual_revenue=business.annual_revenue,
        employee_count=business.employee_count,
        established_year=business.established_year,
        city=business.city,
        state=business.state
    )


class BusinessCreate(BaseModel):
    """Business creation model"""
    business_name: str
    industry: str
    business_size: str
    legal_name: Optional[str] = None
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None
    established_year: Optional[int] = None


class BusinessCreateWithUser(BaseModel):
    """Business creation with user ID"""
    user_id: int
    business_name: str
    industry: str
    business_size: str
    legal_name: Optional[str] = None
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None
    established_year: Optional[int] = None


@router.post("/", response_model=BusinessResponse)
async def create_business(
    business_data: BusinessCreateWithUser,
    db: Session = Depends(get_db)
):
    """Create new business"""
    try:
        # Convert string to enum
        industry_enum = IndustryType(business_data.industry)
        size_enum = BusinessSize(business_data.business_size)
        
        new_business = Business(
            user_id=business_data.user_id,
            business_name=business_data.business_name,
            legal_name=business_data.legal_name,
            industry=industry_enum,
            business_size=size_enum,
            gst_number=business_data.gst_number,
            pan_number=business_data.pan_number,
            address=business_data.address,
            city=business_data.city,
            state=business_data.state,
            pincode=business_data.pincode,
            phone=business_data.phone,
            email=business_data.email,
            website=business_data.website,
            annual_revenue=business_data.annual_revenue,
            employee_count=business_data.employee_count,
            established_year=business_data.established_year
        )
        
        db.add(new_business)
        db.commit()
        db.refresh(new_business)
        
        return BusinessResponse(
            id=new_business.id,
            business_name=new_business.business_name,
            legal_name=new_business.legal_name,
            industry=new_business.industry.value,
            business_size=new_business.business_size.value,
            gst_number=new_business.gst_number,
            annual_revenue=new_business.annual_revenue,
            employee_count=new_business.employee_count,
            established_year=new_business.established_year,
            city=new_business.city,
            state=new_business.state
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid industry or business size: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create business: {str(e)}")
