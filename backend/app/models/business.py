"""
Business and Financial models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class IndustryType(str, enum.Enum):
    """Industry classification"""
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    AGRICULTURE = "agriculture"
    SERVICES = "services"
    LOGISTICS = "logistics"
    ECOMMERCE = "ecommerce"
    HOSPITALITY = "hospitality"
    HEALTHCARE = "healthcare"
    TECHNOLOGY = "technology"
    CONSTRUCTION = "construction"
    OTHER = "other"


class BusinessSize(str, enum.Enum):
    """Business size classification"""
    MICRO = "micro"  # < 10 employees
    SMALL = "small"  # 10-50 employees
    MEDIUM = "medium"  # 50-250 employees


class Business(Base):
    """Business entity model"""
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Basic information
    business_name = Column(String, nullable=False)
    legal_name = Column(String, nullable=True)
    registration_number = Column(String, nullable=True)
    gst_number = Column(String, nullable=True, index=True)
    pan_number = Column(String, nullable=True)
    
    # Classification
    industry = Column(Enum(IndustryType), nullable=False)
    business_size = Column(Enum(BusinessSize), default=BusinessSize.SMALL)
    
    # Contact information
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    
    # Business metrics
    annual_revenue = Column(Float, nullable=True)
    employee_count = Column(Integer, nullable=True)
    established_year = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="businesses")
    financial_data = relationship("FinancialData", back_populates="business", cascade="all, delete-orphan")
    assessments = relationship("FinancialAssessment", back_populates="business", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="business", cascade="all, delete-orphan")


class FinancialData(Base):
    """Financial statements and data"""
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Period information
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=True)  # 1-4 for quarterly data
    
    # Revenue
    total_revenue = Column(Float, default=0.0)
    revenue_breakdown = Column(JSON, nullable=True)  # {"product_a": 1000, "service_b": 2000}
    
    # Expenses
    total_expenses = Column(Float, default=0.0)
    cost_of_goods_sold = Column(Float, default=0.0)
    operating_expenses = Column(Float, default=0.0)
    salaries_wages = Column(Float, default=0.0)
    rent = Column(Float, default=0.0)
    utilities = Column(Float, default=0.0)
    marketing = Column(Float, default=0.0)
    other_expenses = Column(Float, default=0.0)
    expense_breakdown = Column(JSON, nullable=True)
    
    # Assets
    total_assets = Column(Float, default=0.0)
    current_assets = Column(Float, default=0.0)
    cash_and_equivalents = Column(Float, default=0.0)
    accounts_receivable = Column(Float, default=0.0)
    inventory = Column(Float, default=0.0)
    fixed_assets = Column(Float, default=0.0)
    
    # Liabilities
    total_liabilities = Column(Float, default=0.0)
    current_liabilities = Column(Float, default=0.0)
    accounts_payable = Column(Float, default=0.0)
    short_term_debt = Column(Float, default=0.0)
    long_term_debt = Column(Float, default=0.0)
    
    # Equity
    owners_equity = Column(Float, default=0.0)
    
    # Cash Flow
    operating_cash_flow = Column(Float, default=0.0)
    investing_cash_flow = Column(Float, default=0.0)
    financing_cash_flow = Column(Float, default=0.0)
    
    # Tax information
    tax_paid = Column(Float, default=0.0)
    tax_deductions = Column(Float, default=0.0)
    gst_collected = Column(Float, default=0.0)
    gst_paid = Column(Float, default=0.0)
    
    # Metadata
    data_source = Column(String, nullable=True)  # "manual", "csv", "api", "gst"
    is_verified = Column(Boolean, default=False)
    uploaded_file_path = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="financial_data")


class Transaction(Base):
    """Individual transactions"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Transaction details
    transaction_date = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=True)  # "revenue", "expense", "asset", "liability"
    subcategory = Column(String, nullable=True)
    
    # Amounts
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    
    # Payment information
    payment_method = Column(String, nullable=True)  # "cash", "bank", "upi", "card"
    reference_number = Column(String, nullable=True)
    
    # Tax
    is_taxable = Column(Boolean, default=True)
    tax_amount = Column(Float, default=0.0)
    gst_rate = Column(Float, default=0.0)
    
    # Metadata
    source = Column(String, nullable=True)  # "manual", "bank_api", "payment_gateway"
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="transactions")
