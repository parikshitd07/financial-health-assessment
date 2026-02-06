"""Assessment Routes"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.assessment import FinancialAssessment
from app.models.business import Business

router = APIRouter()


@router.get("/business/{business_id}")
async def get_assessments_by_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get all assessments for a business"""
    # Check if business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Get all assessments for this business
    assessments = db.query(FinancialAssessment).filter(
        FinancialAssessment.business_id == business_id
    ).order_by(FinancialAssessment.assessment_date.desc()).all()
    
    return {
        "success": True,
        "business_id": business_id,
        "business_name": business.business_name,
        "count": len(assessments),
        "assessments": [{
            "id": a.id,
            "assessment_date": a.assessment_date,
            "overall_health_score": a.overall_health_score,
            "creditworthiness_score": a.creditworthiness_score,
            "liquidity_score": a.liquidity_score,
            "profitability_score": a.profitability_score,
            "efficiency_score": a.efficiency_score,
            "credit_rating": a.credit_rating,
            "risk_level": a.risk_level,
            "ai_summary": a.ai_summary,
            "strengths": a.strengths,
            "weaknesses": a.weaknesses,
            "opportunities": a.opportunities,
            "threats": a.threats,
            "cost_optimization_recommendations": a.cost_optimization_recommendations,
            "revenue_enhancement_recommendations": a.revenue_enhancement_recommendations,
            "working_capital_recommendations": a.working_capital_recommendations,
            "tax_optimization_recommendations": a.tax_optimization_recommendations,
            "recommended_products": a.recommended_products,
            "identified_risks": a.identified_risks,
            "risk_mitigation_strategies": a.risk_mitigation_strategies,
            "revenue_forecast_3m": a.revenue_forecast_3m,
            "revenue_forecast_6m": a.revenue_forecast_6m,
            "revenue_forecast_12m": a.revenue_forecast_12m,
            "cash_flow_forecast_3m": a.cash_flow_forecast_3m,
            "tax_compliance_score": a.tax_compliance_score,
            "compliance_issues": a.compliance_issues,
            "percentile_rank": a.percentile_rank,
            "ai_model_used": a.ai_model_used,
            "ai_confidence_score": a.ai_confidence_score
        } for a in assessments]
    }


@router.get("/latest/{business_id}")
async def get_latest_assessment(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get the latest assessment for a business"""
    # Check if business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Get latest assessment
    assessment = db.query(FinancialAssessment).filter(
        FinancialAssessment.business_id == business_id
    ).order_by(FinancialAssessment.assessment_date.desc()).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No assessment found for this business")
    
    return {
        "success": True,
        "business_id": business_id,
        "business_name": business.business_name,
        "assessment": {
            "id": assessment.id,
            "assessment_date": assessment.assessment_date,
            "overall_health_score": assessment.overall_health_score,
            "creditworthiness_score": assessment.creditworthiness_score,
            "liquidity_score": assessment.liquidity_score,
            "profitability_score": assessment.profitability_score,
            "efficiency_score": assessment.efficiency_score,
            "credit_rating": assessment.credit_rating,
            "risk_level": assessment.risk_level,
            "ai_summary": assessment.ai_summary,
            "strengths": assessment.strengths,
            "weaknesses": assessment.weaknesses,
            "opportunities": assessment.opportunities,
            "threats": assessment.threats,
            "cost_optimization_recommendations": assessment.cost_optimization_recommendations,
            "revenue_enhancement_recommendations": assessment.revenue_enhancement_recommendations,
            "working_capital_recommendations": assessment.working_capital_recommendations,
            "tax_optimization_recommendations": assessment.tax_optimization_recommendations,
            "recommended_products": assessment.recommended_products,
            "identified_risks": assessment.identified_risks,
            "risk_mitigation_strategies": assessment.risk_mitigation_strategies,
            "revenue_forecast_3m": assessment.revenue_forecast_3m,
            "revenue_forecast_6m": assessment.revenue_forecast_6m,
            "revenue_forecast_12m": assessment.revenue_forecast_12m,
            "cash_flow_forecast_3m": assessment.cash_flow_forecast_3m,
            "tax_compliance_score": assessment.tax_compliance_score,
            "compliance_issues": assessment.compliance_issues,
            "percentile_rank": assessment.percentile_rank,
            "ai_model_used": assessment.ai_model_used,
            "ai_confidence_score": assessment.ai_confidence_score
        }
    }


@router.get("/{assessment_id}")
async def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """Get specific assessment by ID"""
    assessment = db.query(FinancialAssessment).filter(
        FinancialAssessment.id == assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return {
        "success": True,
        "assessment": {
            "id": assessment.id,
            "business_id": assessment.business_id,
            "assessment_date": assessment.assessment_date,
            "overall_health_score": assessment.overall_health_score,
            "creditworthiness_score": assessment.creditworthiness_score,
            "liquidity_score": assessment.liquidity_score,
            "profitability_score": assessment.profitability_score,
            "efficiency_score": assessment.efficiency_score,
            "credit_rating": assessment.credit_rating,
            "risk_level": assessment.risk_level,
            "ai_summary": assessment.ai_summary,
            "strengths": assessment.strengths,
            "weaknesses": assessment.weaknesses,
            "opportunities": assessment.opportunities,
            "threats": assessment.threats,
            "cost_optimization_recommendations": assessment.cost_optimization_recommendations,
            "revenue_enhancement_recommendations": assessment.revenue_enhancement_recommendations,
            "working_capital_recommendations": assessment.working_capital_recommendations,
            "tax_optimization_recommendations": assessment.tax_optimization_recommendations,
            "recommended_products": assessment.recommended_products,
            "identified_risks": assessment.identified_risks,
            "risk_mitigation_strategies": assessment.risk_mitigation_strategies,
            "revenue_forecast_3m": assessment.revenue_forecast_3m,
            "revenue_forecast_6m": assessment.revenue_forecast_6m,
            "revenue_forecast_12m": assessment.revenue_forecast_12m,
            "cash_flow_forecast_3m": assessment.cash_flow_forecast_3m,
            "tax_compliance_score": assessment.tax_compliance_score,
            "compliance_issues": assessment.compliance_issues,
            "percentile_rank": assessment.percentile_rank,
            "ai_model_used": assessment.ai_model_used,
            "ai_confidence_score": assessment.ai_confidence_score
        }
    }


@router.get("/user/{user_id}/all")
async def get_all_user_assessments(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all assessments for all businesses owned by a user"""
    from app.models.business import Business
    
    # Get all businesses for this user
    businesses = db.query(Business).filter(Business.user_id == user_id).all()
    
    if not businesses:
        return {
            "success": True,
            "user_id": user_id,
            "total_businesses": 0,
            "total_assessments": 0,
            "assessments": []
        }
    
    business_ids = [b.id for b in businesses]
    
    # Get all assessments for these businesses
    assessments = db.query(FinancialAssessment).filter(
        FinancialAssessment.business_id.in_(business_ids)
    ).order_by(FinancialAssessment.assessment_date.desc()).all()
    
    # Create a map of business info
    business_map = {b.id: b for b in businesses}
    
    return {
        "success": True,
        "user_id": user_id,
        "total_businesses": len(businesses),
        "total_assessments": len(assessments),
        "assessments": [{
            "id": a.id,
            "business_id": a.business_id,
            "business_name": business_map[a.business_id].business_name,
            "industry": business_map[a.business_id].industry.value if business_map[a.business_id].industry else "other",
            "assessment_date": a.assessment_date,
            "overall_health_score": a.overall_health_score,
            "creditworthiness_score": a.creditworthiness_score,
            "liquidity_score": a.liquidity_score,
            "profitability_score": a.profitability_score,
            "efficiency_score": a.efficiency_score,
            "credit_rating": a.credit_rating,
            "risk_level": a.risk_level,
            "ai_summary": a.ai_summary,
            "strengths": a.strengths,
            "weaknesses": a.weaknesses,
            "opportunities": a.opportunities,
            "threats": a.threats,
            "cost_optimization_recommendations": a.cost_optimization_recommendations,
            "revenue_enhancement_recommendations": a.revenue_enhancement_recommendations,
            "working_capital_recommendations": a.working_capital_recommendations,
            "tax_optimization_recommendations": a.tax_optimization_recommendations,
            "recommended_products": a.recommended_products,
            "identified_risks": a.identified_risks,
            "risk_mitigation_strategies": a.risk_mitigation_strategies,
            "revenue_forecast_3m": a.revenue_forecast_3m,
            "revenue_forecast_6m": a.revenue_forecast_6m,
            "revenue_forecast_12m": a.revenue_forecast_12m,
            "cash_flow_forecast_3m": a.cash_flow_forecast_3m,
            "tax_compliance_score": a.tax_compliance_score,
            "compliance_issues": a.compliance_issues,
            "percentile_rank": a.percentile_rank,
            "ai_model_used": a.ai_model_used,
            "ai_confidence_score": a.ai_confidence_score
        } for a in assessments]
    }


@router.post("/{business_id}")
async def create_assessment(business_id: int):
    """Manual assessment creation - placeholder"""
    return {
        "success": False,
        "message": "Manual assessment creation not yet implemented. Upload financial data to trigger automatic assessment."
    }
