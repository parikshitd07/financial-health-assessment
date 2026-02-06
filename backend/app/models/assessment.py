"""
Financial Assessment and Report models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class RiskLevel(str, enum.Enum):
    """Risk level classification"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class CreditRating(str, enum.Enum):
    """Credit rating classification"""
    AAA = "AAA"  # Excellent
    AA = "AA"    # Very Good
    A = "A"      # Good
    BBB = "BBB"  # Adequate
    BB = "BB"    # Speculative
    B = "B"      # Highly Speculative
    CCC = "CCC"  # Vulnerable
    CC = "CC"    # Very Vulnerable
    C = "C"      # Extremely Vulnerable
    D = "D"      # Default


class FinancialAssessment(Base):
    """AI-powered financial health assessment"""
    __tablename__ = "financial_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Assessment period
    assessment_date = Column(DateTime, default=datetime.utcnow)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Overall scores (0-100)
    overall_health_score = Column(Float, nullable=False)
    creditworthiness_score = Column(Float, nullable=False)
    liquidity_score = Column(Float, nullable=False)
    profitability_score = Column(Float, nullable=False)
    efficiency_score = Column(Float, nullable=False)
    
    # Credit rating
    credit_rating = Column(Enum(CreditRating), nullable=False)
    risk_level = Column(Enum(RiskLevel), nullable=False)
    
    # Financial ratios
    current_ratio = Column(Float, nullable=True)
    quick_ratio = Column(Float, nullable=True)
    debt_to_equity = Column(Float, nullable=True)
    debt_to_asset = Column(Float, nullable=True)
    return_on_assets = Column(Float, nullable=True)
    return_on_equity = Column(Float, nullable=True)
    gross_profit_margin = Column(Float, nullable=True)
    net_profit_margin = Column(Float, nullable=True)
    operating_margin = Column(Float, nullable=True)
    asset_turnover = Column(Float, nullable=True)
    inventory_turnover = Column(Float, nullable=True)
    receivables_turnover = Column(Float, nullable=True)
    
    # Working capital
    working_capital = Column(Float, nullable=True)
    working_capital_ratio = Column(Float, nullable=True)
    cash_conversion_cycle = Column(Integer, nullable=True)  # in days
    
    # Cash flow metrics
    operating_cash_flow_ratio = Column(Float, nullable=True)
    free_cash_flow = Column(Float, nullable=True)
    
    # AI-generated insights
    ai_summary = Column(Text, nullable=True)
    strengths = Column(JSON, nullable=True)  # List of strengths
    weaknesses = Column(JSON, nullable=True)  # List of weaknesses
    opportunities = Column(JSON, nullable=True)  # List of opportunities
    threats = Column(JSON, nullable=True)  # List of threats
    
    # Recommendations
    cost_optimization_recommendations = Column(JSON, nullable=True)
    revenue_enhancement_recommendations = Column(JSON, nullable=True)
    working_capital_recommendations = Column(JSON, nullable=True)
    tax_optimization_recommendations = Column(JSON, nullable=True)
    
    # Financial product recommendations
    recommended_products = Column(JSON, nullable=True)
    """
    Example:
    [
        {
            "product_type": "working_capital_loan",
            "provider": "HDFC Bank",
            "amount": 500000,
            "interest_rate": 12.5,
            "reason": "To improve cash flow during peak season"
        }
    ]
    """
    
    # Risk assessment
    identified_risks = Column(JSON, nullable=True)
    risk_mitigation_strategies = Column(JSON, nullable=True)
    
    # Industry benchmarking
    industry_comparison = Column(JSON, nullable=True)
    percentile_rank = Column(Float, nullable=True)  # 0-100
    
    # Forecasting
    revenue_forecast_3m = Column(Float, nullable=True)
    revenue_forecast_6m = Column(Float, nullable=True)
    revenue_forecast_12m = Column(Float, nullable=True)
    cash_flow_forecast_3m = Column(Float, nullable=True)
    
    # Compliance
    tax_compliance_score = Column(Float, nullable=True)  # 0-100
    compliance_issues = Column(JSON, nullable=True)
    
    # AI model metadata
    ai_model_used = Column(String, nullable=True)  # "gpt-4", "claude-3-opus"
    ai_confidence_score = Column(Float, nullable=True)  # 0-1
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="assessments")


class FinancialReport(Base):
    """Generated financial reports"""
    __tablename__ = "financial_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("financial_assessments.id"), nullable=True)
    
    # Report details
    report_name = Column(String, nullable=False)
    report_type = Column(String, nullable=False)  # "investor", "bank", "tax", "compliance"
    language = Column(String, default="en")  # "en", "hi", etc.
    
    # Content
    report_data = Column(JSON, nullable=False)
    summary = Column(Text, nullable=True)
    
    # File storage
    pdf_path = Column(String, nullable=True)
    excel_path = Column(String, nullable=True)
    
    # Metadata
    is_public = Column(Boolean, default=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="financial_reports")


class IndustryBenchmark(Base):
    """Industry-specific benchmark data"""
    __tablename__ = "industry_benchmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Industry classification
    industry = Column(String, nullable=False, index=True)
    business_size = Column(String, nullable=False)  # "micro", "small", "medium"
    
    # Period
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=True)
    
    # Benchmark metrics (median values)
    current_ratio_median = Column(Float, nullable=True)
    debt_to_equity_median = Column(Float, nullable=True)
    gross_margin_median = Column(Float, nullable=True)
    net_margin_median = Column(Float, nullable=True)
    roa_median = Column(Float, nullable=True)
    roe_median = Column(Float, nullable=True)
    inventory_turnover_median = Column(Float, nullable=True)
    receivables_days_median = Column(Integer, nullable=True)
    payables_days_median = Column(Integer, nullable=True)
    
    # Percentile data
    percentile_data = Column(JSON, nullable=True)
    """
    Example:
    {
        "current_ratio": {"p25": 1.2, "p50": 1.5, "p75": 2.0},
        "gross_margin": {"p25": 25, "p50": 35, "p75": 45}
    }
    """
    
    # Sample size
    sample_size = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
