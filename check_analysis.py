#!/usr/bin/env python3
"""
Check if AI analysis results are in the database
"""
import sys
import os

os.chdir('backend')
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.assessment import FinancialAssessment
from app.models.business import FinancialData

print("Checking database for analysis results...")
print("=" * 80)

db = SessionLocal()

try:
    # Check uploaded financial data
    financial_data = db.query(FinancialData).all()
    print(f"\n📊 Uploaded Financial Data Records: {len(financial_data)}")
    for fd in financial_data:
        print(f"  - ID: {fd.id}, Business: {fd.business_id}, Fiscal Year: {fd.fiscal_year}")
        print(f"    Total Revenue: ₹{fd.total_revenue:,.2f}")
        print(f"    Total Assets: ₹{fd.total_assets:,.2f}")
        print(f"    Uploaded: {fd.created_at}")
    
    # Check AI analysis results
    assessments = db.query(FinancialAssessment).all()
    print(f"\n🤖 AI Analysis Results: {len(assessments)}")
    
    if assessments:
        for assessment in assessments:
            print(f"\n  Assessment ID: {assessment.id}")
            print(f"  Business ID: {assessment.business_id}")
            print(f"  Assessment Date: {assessment.assessment_date}")
            print(f"  Overall Health Score: {assessment.overall_health_score:.2f}/100")
            print(f"  Credit Rating: {assessment.credit_rating}")
            print(f"  Risk Level: {assessment.risk_level}")
            print(f"  Liquidity Score: {assessment.liquidity_score:.2f}/100")
            print(f"  Profitability Score: {assessment.profitability_score:.2f}/100")
            print(f"  Efficiency Score: {assessment.efficiency_score:.2f}/100")
            print(f"  AI Model Used: {assessment.ai_model_used}")
            
            if assessment.strengths:
                print(f"\n  ✅ Strengths ({len(assessment.strengths)}):")
                for i, strength in enumerate(assessment.strengths[:3], 1):
                    print(f"    {i}. {strength}")
            
            if assessment.weaknesses:
                print(f"\n  ⚠️  Weaknesses ({len(assessment.weaknesses)}):")
                for i, weakness in enumerate(assessment.weaknesses[:3], 1):
                    print(f"    {i}. {weakness}")
            
            if assessment.ai_summary:
                print(f"\n  📝 AI Summary:")
                print(f"    {assessment.ai_summary[:200]}...")
            
            print("\n  " + "-" * 76)
    else:
        print("\n  ⏳ No AI analysis results found yet.")
        print("  Upload a file and wait 30 seconds for analysis to complete.")
    
    print("\n" + "=" * 80)
    print("✅ Database check complete!")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
