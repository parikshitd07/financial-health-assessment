"""
AI-powered Financial Analysis Service
Integrates with Google Gemini 3 Flash, OpenAI GPT-4, and Claude for intelligent financial insights
"""
from typing import Dict, Any, List, Optional
import json
from google import genai
from google.genai import types

from app.core.config import settings


class AIAnalysisService:
    """Service for AI-powered financial analysis"""
    
    def __init__(self):
        # Initialize Gemini client (primary)
        if settings.GEMINI_API_KEY:
            self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        else:
            self.gemini_client = None
        
        # Initialize OpenAI client (fallback)
        if settings.OPENAI_API_KEY:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.openai_client = None
        
        # Initialize Claude client (fallback)
        if settings.CLAUDE_API_KEY:
            from anthropic import Anthropic
            self.claude_client = Anthropic(api_key=settings.CLAUDE_API_KEY)
        else:
            self.claude_client = None
        
        self.model = settings.AI_MODEL
    
    def analyze_financial_health(
        self,
        financial_data: Dict[str, Any],
        business_info: Dict[str, Any],
        industry_benchmarks: Optional[Dict[str, Any]] = None,
        pdf_bytes: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive AI analysis of financial health
        
        Args:
            financial_data: Financial statements and metrics
            business_info: Business profile information
            industry_benchmarks: Industry comparison data
            pdf_bytes: Raw PDF bytes for direct analysis (if PDF uploaded)
        
        Returns:
            Comprehensive analysis with insights and recommendations
        """
        # If PDF bytes provided, send directly to Gemini
        if pdf_bytes and self.gemini_client:
            return self._analyze_pdf_with_gemini(pdf_bytes, business_info)
        
        # Otherwise use traditional text-based analysis
        prompt = self._create_analysis_prompt(financial_data, business_info, industry_benchmarks)
        
        # Priority: Gemini > GPT > Claude
        if "gemini" in self.model.lower() and self.gemini_client:
            return self._analyze_with_gemini(prompt)
        elif "gpt" in self.model.lower() and self.openai_client:
            return self._analyze_with_gpt(prompt)
        elif "claude" in self.model.lower() and self.claude_client:
            return self._analyze_with_claude(prompt)
        elif self.gemini_client:
            return self._analyze_with_gemini(prompt)  # Default to Gemini if available
        elif self.openai_client:
            return self._analyze_with_gpt(prompt)  # Fallback to GPT
        else:
            raise Exception("No AI provider configured. Please set GEMINI_API_KEY, OPENAI_API_KEY, or CLAUDE_API_KEY")
    
    def _create_analysis_prompt(
        self,
        financial_data: Dict[str, Any],
        business_info: Dict[str, Any],
        industry_benchmarks: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create detailed prompt for AI analysis"""
        
        prompt = f"""
You are an expert financial analyst specializing in SME financial health assessment. 
Analyze the following financial data and provide comprehensive insights.

BUSINESS INFORMATION:
- Business Name: {business_info.get('business_name')}
- Industry: {business_info.get('industry')}
- Business Size: {business_info.get('business_size')}
- Years in Operation: {business_info.get('years_in_operation', 'N/A')}

FINANCIAL DATA:
Revenue: ₹{financial_data.get('total_revenue', 0):,.2f}
Expenses: ₹{financial_data.get('total_expenses', 0):,.2f}
Net Profit: ₹{financial_data.get('total_revenue', 0) - financial_data.get('total_expenses', 0):,.2f}

Assets:
- Total Assets: ₹{financial_data.get('total_assets', 0):,.2f}
- Current Assets: ₹{financial_data.get('current_assets', 0):,.2f}
- Cash: ₹{financial_data.get('cash_and_equivalents', 0):,.2f}
- Receivables: ₹{financial_data.get('accounts_receivable', 0):,.2f}
- Inventory: ₹{financial_data.get('inventory', 0):,.2f}

Liabilities:
- Total Liabilities: ₹{financial_data.get('total_liabilities', 0):,.2f}
- Current Liabilities: ₹{financial_data.get('current_liabilities', 0):,.2f}
- Accounts Payable: ₹{financial_data.get('accounts_payable', 0):,.2f}
- Short-term Debt: ₹{financial_data.get('short_term_debt', 0):,.2f}
- Long-term Debt: ₹{financial_data.get('long_term_debt', 0):,.2f}

Cash Flow:
- Operating Cash Flow: ₹{financial_data.get('operating_cash_flow', 0):,.2f}
- Investing Cash Flow: ₹{financial_data.get('investing_cash_flow', 0):,.2f}
- Financing Cash Flow: ₹{financial_data.get('financing_cash_flow', 0):,.2f}

Tax Information:
- Tax Paid: ₹{financial_data.get('tax_paid', 0):,.2f}
- GST Collected: ₹{financial_data.get('gst_collected', 0):,.2f}
- GST Paid: ₹{financial_data.get('gst_paid', 0):,.2f}
"""

        if industry_benchmarks:
            prompt += f"""
INDUSTRY BENCHMARKS ({business_info.get('industry')}):
- Median Current Ratio: {industry_benchmarks.get('current_ratio_median', 'N/A')}
- Median Gross Margin: {industry_benchmarks.get('gross_margin_median', 'N/A')}%
- Median Net Margin: {industry_benchmarks.get('net_margin_median', 'N/A')}%
- Median Debt-to-Equity: {industry_benchmarks.get('debt_to_equity_median', 'N/A')}
"""

        prompt += """

Please provide a comprehensive financial health assessment in the following JSON format:

{
  "overall_health_score": <0-100>,
  "creditworthiness_score": <0-100>,
  "liquidity_score": <0-100>,
  "profitability_score": <0-100>,
  "efficiency_score": <0-100>,
  "credit_rating": "<AAA|AA|A|BBB|BB|B|CCC|CC|C|D>",
  "risk_level": "<low|moderate|high|critical>",
  "ai_summary": "<2-3 paragraph executive summary>",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2", "weakness3"],
  "opportunities": ["opportunity1", "opportunity2", "opportunity3"],
  "threats": ["threat1", "threat2", "threat3"],
  "cost_optimization_recommendations": [
    {"area": "area_name", "recommendation": "detailed_recommendation", "potential_savings": amount}
  ],
  "revenue_enhancement_recommendations": [
    {"strategy": "strategy_name", "recommendation": "detailed_recommendation", "potential_increase": amount}
  ],
  "working_capital_recommendations": [
    {"aspect": "aspect_name", "recommendation": "detailed_recommendation", "impact": "high|medium|low"}
  ],
  "tax_optimization_recommendations": [
    {"area": "area_name", "recommendation": "detailed_recommendation", "potential_savings": amount}
  ],
  "recommended_products": [
    {
      "product_type": "loan_type",
      "provider": "bank_name",
      "amount": suggested_amount,
      "interest_rate": estimated_rate,
      "reason": "why_this_product"
    }
  ],
  "identified_risks": [
    {"risk": "risk_description", "severity": "high|medium|low", "probability": "high|medium|low"}
  ],
  "risk_mitigation_strategies": [
    {"risk": "risk_name", "strategy": "mitigation_strategy"}
  ],
  "revenue_forecast_3m": estimated_amount,
  "revenue_forecast_6m": estimated_amount,
  "revenue_forecast_12m": estimated_amount,
  "cash_flow_forecast_3m": estimated_amount,
  "tax_compliance_score": <0-100>,
  "compliance_issues": ["issue1", "issue2"],
  "percentile_rank": <0-100 compared to industry>,
  "ai_confidence_score": <0-1>
}

Provide actionable, specific recommendations tailored to Indian SMEs. Consider GST compliance, working capital challenges, and growth opportunities.
"""
        return prompt
    
    def _analyze_pdf_with_gemini(self, pdf_bytes: bytes, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze PDF directly with Gemini 3 using native PDF support"""
        try:
            import base64
            
            # Create the analysis prompt
            analysis_prompt = f"""
You are an expert financial analyst specializing in SME financial health assessment.

BUSINESS INFORMATION:
- Business Name: {business_info.get('business_name')}
- Industry: {business_info.get('industry')}
- Business Size: {business_info.get('business_size')}

Analyze the financial document provided and extract ALL financial metrics including:
- Revenue, expenses, profit/loss
- Assets (current, fixed, total)
- Liabilities (current, long-term, total)
- Cash flow information
- Any other relevant financial data

Then provide a comprehensive financial health assessment in the following JSON format:

{{
  "overall_health_score": <0-100>,
  "creditworthiness_score": <0-100>,
  "liquidity_score": <0-100>,
  "profitability_score": <0-100>,
  "efficiency_score": <0-100>,
  "credit_rating": "<AAA|AA|A|BBB|BB|B|CCC|CC|C|D>",
  "risk_level": "<low|moderate|high|critical>",
  "ai_summary": "<2-3 paragraph executive summary>",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2", "weakness3"],
  "opportunities": ["opportunity1", "opportunity2", "opportunity3"],
  "threats": ["threat1", "threat2", "threat3"],
  "cost_optimization_recommendations": [
    {{"area": "area_name", "recommendation": "detailed_recommendation", "potential_savings": amount}}
  ],
  "revenue_enhancement_recommendations": [
    {{"strategy": "strategy_name", "recommendation": "detailed_recommendation", "potential_increase": amount}}
  ],
  "working_capital_recommendations": [
    {{"aspect": "aspect_name", "recommendation": "detailed_recommendation", "impact": "high|medium|low"}}
  ],
  "tax_optimization_recommendations": [
    {{"area": "area_name", "recommendation": "detailed_recommendation", "potential_savings": amount}}
  ],
  "recommended_products": [
    {{
      "product_type": "loan_type",
      "provider": "bank_name",
      "amount": suggested_amount,
      "interest_rate": estimated_rate,
      "reason": "why_this_product"
    }}
  ],
  "identified_risks": [
    {{"risk": "risk_description", "severity": "high|medium|low", "probability": "high|medium|low"}}
  ],
  "risk_mitigation_strategies": [
    {{"risk": "risk_name", "strategy": "mitigation_strategy"}}
  ],
  "revenue_forecast_3m": estimated_amount,
  "revenue_forecast_6m": estimated_amount,
  "revenue_forecast_12m": estimated_amount,
  "cash_flow_forecast_3m": estimated_amount,
  "tax_compliance_score": <0-100>,
  "compliance_issues": ["issue1", "issue2"],
  "percentile_rank": <0-100 compared to industry>,
  "ai_confidence_score": <0-1>
}}

Provide actionable, specific recommendations tailored to Indian SMEs. Consider GST compliance, working capital challenges, and growth opportunities.
"""
            
            # Use v1alpha API for media_resolution support
            client = genai.Client(
                api_key=settings.GEMINI_API_KEY,
                http_options={'api_version': 'v1alpha'}
            )
            
            # Send PDF directly to Gemini with optimal resolution for documents
            response = client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        parts=[
                            types.Part(text=analysis_prompt),
                            types.Part(
                                inline_data=types.Blob(
                                    mime_type="application/pdf",
                                    data=pdf_bytes,
                                ),
                                media_resolution={"level": "media_resolution_medium"}
                            )
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            result["ai_model_used"] = self.model
            return result
        
        except Exception as e:
            raise Exception(f"Gemini PDF analysis failed: {str(e)}")
    
    def _analyze_with_gemini(self, prompt: str) -> Dict[str, Any]:
        """Analyze using Google Gemini 3 Flash"""
        try:
            response = self.gemini_client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    response_mime_type="application/json"
                )
            )
            
            result = json.loads(response.text)
            result["ai_model_used"] = self.model
            return result
        
        except Exception as e:
            raise Exception(f"Gemini analysis failed: {str(e)}")
    
    def _analyze_with_gpt(self, prompt: str) -> Dict[str, Any]:
        """Analyze using OpenAI GPT"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial analyst specializing in SME financial health assessment for Indian businesses. Provide detailed, actionable insights in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            result["ai_model_used"] = self.model
            return result
        
        except Exception as e:
            raise Exception(f"GPT analysis failed: {str(e)}")
    
    def _analyze_with_claude(self, prompt: str) -> Dict[str, Any]:
        """Analyze using Claude"""
        try:
            response = self.claude_client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            
            content = response.content[0].text
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            result = json.loads(content)
            result["ai_model_used"] = self.model
            return result
        
        except Exception as e:
            raise Exception(f"Claude analysis failed: {str(e)}")
    
    def generate_narrative_report(
        self,
        assessment: Dict[str, Any],
        language: str = "en"
    ) -> str:
        """
        Generate narrative financial report
        
        Args:
            assessment: Financial assessment data
            language: Language code (en, hi, etc.)
        
        Returns:
            Formatted narrative report
        """
        prompt = f"""
Generate a comprehensive financial health report based on the following assessment data:

{json.dumps(assessment, indent=2)}

Language: {language}

Create a professional, easy-to-understand report suitable for business owners who may not have financial expertise.
Include sections for:
1. Executive Summary
2. Financial Health Overview
3. Key Strengths and Weaknesses
4. Risk Assessment
5. Recommendations for Improvement
6. Financial Product Suggestions
7. Future Outlook

Make it concise yet comprehensive, approximately 1500-2000 words.
"""
        
        if "gpt" in self.model.lower():
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional financial report writer. Write clear, actionable reports in {language}."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5
            )
            return response.choices[0].message.content
        
        elif self.claude_client:
            response = self.claude_client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5
            )
            return response.content[0].text
    
    def translate_content(self, content: str, target_language: str) -> str:
        """
        Translate content to target language
        
        Args:
            content: Content to translate
            target_language: Target language code
        
        Returns:
            Translated content
        """
        language_names = {
            "hi": "Hindi",
            "en": "English",
            "ta": "Tamil",
            "te": "Telugu",
            "mr": "Marathi",
            "gu": "Gujarati"
        }
        
        lang_name = language_names.get(target_language, target_language)
        
        prompt = f"""
Translate the following financial content to {lang_name}. 
Maintain professional terminology and accuracy:

{content}
"""
        
        if "gpt" in self.model.lower():
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional translator specializing in financial content. Translate to {lang_name}."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        
        elif self.claude_client:
            response = self.claude_client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            return response.content[0].text
        
        return content  # Fallback


# Create singleton instance
ai_service = AIAnalysisService()
