"""
User model for authentication and authorization
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    BUSINESS_OWNER = "business_owner"
    ACCOUNTANT = "accountant"
    VIEWER = "viewer"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.BUSINESS_OWNER, nullable=False)
    
    # Profile fields
    phone = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # API Key for integrations
    api_key = Column(String, nullable=True, unique=True)
    
    # Relationships
    businesses = relationship("Business", back_populates="owner", cascade="all, delete-orphan")
    financial_reports = relationship("FinancialReport", back_populates="user", cascade="all, delete-orphan")
