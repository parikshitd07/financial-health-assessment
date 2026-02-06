"""Financial Data Routes"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.models.business import FinancialData, Business
from app.services.file_parser import file_parser
from app.services.financial_analysis import financial_service
from app.services.ai_analysis import ai_service

router = APIRouter()

# Upload directory
UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def analyze_financial_data_background(
    financial_data_id: int,
    parsed_data: dict,
    business_id: int
):
    """Background task to analyze financial data with AI"""
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Get financial data record
        fin_data = db.query(FinancialData).filter(FinancialData.id == financial_data_id).first()
        if not fin_data:
            return
        
        # Get business info
        business = db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return
        
        business_info = {
            'business_name': business.business_name,
            'industry': business.industry.value if business.industry else 'other',
            'business_size': business.business_size.value if business.business_size else 'small',
            'years_in_operation': datetime.now().year - business.established_year if business.established_year else 0
        }
        
        # Prepare financial data dict
        financial_dict = {
            'total_revenue': fin_data.total_revenue,
            'total_expenses': fin_data.total_expenses,
            'total_assets': fin_data.total_assets,
            'current_assets': fin_data.current_assets,
            'cash_and_equivalents': fin_data.cash_and_equivalents,
            'accounts_receivable': fin_data.accounts_receivable,
            'inventory': fin_data.inventory,
            'total_liabilities': fin_data.total_liabilities,
            'current_liabilities': fin_data.current_liabilities,
            'accounts_payable': fin_data.accounts_payable,
            'short_term_debt': fin_data.short_term_debt,
            'long_term_debt': fin_data.long_term_debt,
            'owners_equity': fin_data.owners_equity,
            'operating_cash_flow': fin_data.operating_cash_flow,
            'cost_of_goods_sold': fin_data.cost_of_goods_sold,
        }
        
        # Calculate ratios
        ratios = financial_service.calculate_financial_ratios(financial_dict)
        
        # Perform AI analysis
        try:
            # Check if PDF was uploaded
            pdf_bytes = None
            if parsed_data.get('document_type') == 'pdf' and 'raw_pdf_bytes' in parsed_data:
                pdf_bytes = parsed_data['raw_pdf_bytes']
            
            ai_analysis = ai_service.analyze_financial_health(
                financial_dict,
                business_info,
                None,  # No industry benchmarks for now
                pdf_bytes=pdf_bytes  # Pass PDF bytes if available
            )
            
            # Store analysis results in the assessment table
            from app.models.assessment import FinancialAssessment
            
            assessment = FinancialAssessment(
                business_id=business_id,
                assessment_date=datetime.utcnow(),
                period_start=fin_data.period_start,
                period_end=fin_data.period_end,
                creditworthiness_score=ai_analysis.get('creditworthiness_score', 0),
                overall_health_score=ai_analysis.get('overall_health_score', 0),
                liquidity_score=ai_analysis.get('liquidity_score', 0),
                profitability_score=ai_analysis.get('profitability_score', 0),
                efficiency_score=ai_analysis.get('efficiency_score', 0),
                credit_rating=ai_analysis.get('credit_rating', 'BBB'),
                risk_level=ai_analysis.get('risk_level', 'moderate'),
                strengths=ai_analysis.get('strengths', []),
                weaknesses=ai_analysis.get('weaknesses', []),
                opportunities=ai_analysis.get('opportunities', []),
                threats=ai_analysis.get('threats', []),
                cost_optimization_recommendations=ai_analysis.get('cost_optimization_recommendations', []),
                revenue_enhancement_recommendations=ai_analysis.get('revenue_enhancement_recommendations', []),
                working_capital_recommendations=ai_analysis.get('working_capital_recommendations', []),
                tax_optimization_recommendations=ai_analysis.get('tax_optimization_recommendations', []),
                recommended_products=ai_analysis.get('recommended_products', []),
                identified_risks=ai_analysis.get('identified_risks', []),
                risk_mitigation_strategies=ai_analysis.get('risk_mitigation_strategies', []),
                revenue_forecast_3m=ai_analysis.get('revenue_forecast_3m'),
                revenue_forecast_6m=ai_analysis.get('revenue_forecast_6m'),
                revenue_forecast_12m=ai_analysis.get('revenue_forecast_12m'),
                cash_flow_forecast_3m=ai_analysis.get('cash_flow_forecast_3m'),
                tax_compliance_score=ai_analysis.get('tax_compliance_score'),
                compliance_issues=ai_analysis.get('compliance_issues', []),
                percentile_rank=ai_analysis.get('percentile_rank'),
                ai_summary=ai_analysis.get('ai_summary', ''),
                ai_model_used=ai_analysis.get('ai_model_used'),
                ai_confidence_score=ai_analysis.get('ai_confidence_score')
            )
            
            db.add(assessment)
            db.commit()
            
        except Exception as e:
            print(f"AI analysis failed: {str(e)}")
            # Continue even if AI analysis fails
        
    finally:
        db.close()


@router.get("/")
async def get_financial_data(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get all financial data for a business"""
    financial_records = db.query(FinancialData).filter(
        FinancialData.business_id == business_id
    ).order_by(FinancialData.fiscal_year.desc()).all()
    
    return {
        "success": True,
        "count": len(financial_records),
        "data": financial_records
    }


@router.post("/upload")
async def upload_financial_data(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    business_id: int = Form(...),
    fiscal_year: int = Form(...),
    db: Session = Depends(get_db)
):
    """Upload and analyze financial statements"""
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file size (50MB limit)
    file_content = await file.read()
    if len(file_content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 50MB limit")
    
    # Validate file type
    allowed_types = ['text/csv', 'application/vnd.ms-excel', 
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     'application/pdf']
    
    if file.content_type not in allowed_types and not file.filename.endswith(('.csv', '.xlsx', '.xls', '.pdf')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV, Excel, and PDF files are supported")
    
    # Check if business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    try:
        # Parse the file
        parsed_data = file_parser.parse_file(
            file_content,
            file.filename,
            file.content_type or ""
        )
        
        # Save file to disk
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        saved_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, saved_filename)
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Determine period dates
        period_start = datetime(fiscal_year, 1, 1)
        period_end = datetime(fiscal_year, 12, 31)
        
        # Create or update financial data record
        existing = db.query(FinancialData).filter(
            FinancialData.business_id == business_id,
            FinancialData.fiscal_year == fiscal_year
        ).first()
        
        if existing:
            # Update existing record
            for key, value in parsed_data.items():
                if key != 'document_type' and hasattr(existing, key):
                    setattr(existing, key, value)
            
            existing.data_source = 'csv' if file.filename.endswith('.csv') else 'excel' if file.filename.endswith(('.xlsx', '.xls')) else 'pdf'
            existing.uploaded_file_path = file_path
            existing.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(existing)
            financial_data_record = existing
            
        else:
            # Create new record
            financial_data_record = FinancialData(
                business_id=business_id,
                period_start=period_start,
                period_end=period_end,
                fiscal_year=fiscal_year,
                data_source='csv' if file.filename.endswith('.csv') else 'excel' if file.filename.endswith(('.xlsx', '.xls')) else 'pdf',
                uploaded_file_path=file_path,
                **{k: v for k, v in parsed_data.items() if k != 'document_type' and hasattr(FinancialData, k)}
            )
            
            db.add(financial_data_record)
            db.commit()
            db.refresh(financial_data_record)
        
        # Trigger background analysis
        background_tasks.add_task(
            analyze_financial_data_background,
            financial_data_record.id,
            parsed_data,
            business_id
        )
        
        return {
            "success": True,
            "message": "File uploaded successfully. AI analysis is in progress...",
            "file_id": financial_data_record.id,
            "filename": file.filename,
            "document_type": parsed_data.get('document_type', 'unknown'),
            "fiscal_year": fiscal_year,
            "parsed_data": parsed_data,
            "analysis_status": "processing"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/{financial_data_id}")
async def get_financial_data_by_id(
    financial_data_id: int,
    db: Session = Depends(get_db)
):
    """Get specific financial data record"""
    financial_data = db.query(FinancialData).filter(
        FinancialData.id == financial_data_id
    ).first()
    
    if not financial_data:
        raise HTTPException(status_code=404, detail="Financial data not found")
    
    return {
        "success": True,
        "data": financial_data
    }


@router.delete("/{financial_data_id}")
async def delete_financial_data(
    financial_data_id: int,
    db: Session = Depends(get_db)
):
    """Delete financial data record"""
    financial_data = db.query(FinancialData).filter(
        FinancialData.id == financial_data_id
    ).first()
    
    if not financial_data:
        raise HTTPException(status_code=404, detail="Financial data not found")
    
    # Delete file if exists
    if financial_data.uploaded_file_path and os.path.exists(financial_data.uploaded_file_path):
        os.remove(financial_data.uploaded_file_path)
    
    db.delete(financial_data)
    db.commit()
    
    return {
        "success": True,
        "message": "Financial data deleted successfully"
    }
