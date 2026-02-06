"""
Financial Analysis Service
Core financial calculations, ratios, and metrics
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from scipy import stats


class FinancialAnalysisService:
    """Service for financial calculations and analysis"""
    
    def calculate_financial_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate comprehensive financial ratios
        
        Args:
            financial_data: Financial statement data
        
        Returns:
            Dictionary of calculated ratios
        """
        ratios = {}
        
        # Extract data
        total_revenue = financial_data.get('total_revenue', 0)
        total_expenses = financial_data.get('total_expenses', 0)
        cogs = financial_data.get('cost_of_goods_sold', 0)
        total_assets = financial_data.get('total_assets', 0)
        current_assets = financial_data.get('current_assets', 0)
        cash = financial_data.get('cash_and_equivalents', 0)
        receivables = financial_data.get('accounts_receivable', 0)
        inventory = financial_data.get('inventory', 0)
        total_liabilities = financial_data.get('total_liabilities', 0)
        current_liabilities = financial_data.get('current_liabilities', 0)
        payables = financial_data.get('accounts_payable', 0)
        short_term_debt = financial_data.get('short_term_debt', 0)
        long_term_debt = financial_data.get('long_term_debt', 0)
        owners_equity = financial_data.get('owners_equity', 0)
        operating_cash_flow = financial_data.get('operating_cash_flow', 0)
        
        # Net profit
        net_profit = total_revenue - total_expenses
        gross_profit = total_revenue - cogs
        
        # Liquidity Ratios
        ratios['current_ratio'] = current_assets / current_liabilities if current_liabilities > 0 else 0
        ratios['quick_ratio'] = (current_assets - inventory) / current_liabilities if current_liabilities > 0 else 0
        ratios['cash_ratio'] = cash / current_liabilities if current_liabilities > 0 else 0
        
        # Leverage/Solvency Ratios
        total_debt = short_term_debt + long_term_debt
        ratios['debt_to_equity'] = total_debt / owners_equity if owners_equity > 0 else 0
        ratios['debt_to_asset'] = total_liabilities / total_assets if total_assets > 0 else 0
        ratios['equity_multiplier'] = total_assets / owners_equity if owners_equity > 0 else 0
        ratios['debt_ratio'] = total_debt / total_assets if total_assets > 0 else 0
        
        # Profitability Ratios
        ratios['gross_profit_margin'] = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        ratios['net_profit_margin'] = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        ratios['operating_margin'] = ((total_revenue - total_expenses) / total_revenue * 100) if total_revenue > 0 else 0
        ratios['return_on_assets'] = (net_profit / total_assets * 100) if total_assets > 0 else 0
        ratios['return_on_equity'] = (net_profit / owners_equity * 100) if owners_equity > 0 else 0
        
        # Efficiency Ratios
        ratios['asset_turnover'] = total_revenue / total_assets if total_assets > 0 else 0
        ratios['inventory_turnover'] = cogs / inventory if inventory > 0 else 0
        ratios['receivables_turnover'] = total_revenue / receivables if receivables > 0 else 0
        ratios['payables_turnover'] = cogs / payables if payables > 0 else 0
        
        # Days ratios
        ratios['days_sales_outstanding'] = 365 / ratios['receivables_turnover'] if ratios['receivables_turnover'] > 0 else 0
        ratios['days_inventory_outstanding'] = 365 / ratios['inventory_turnover'] if ratios['inventory_turnover'] > 0 else 0
        ratios['days_payables_outstanding'] = 365 / ratios['payables_turnover'] if ratios['payables_turnover'] > 0 else 0
        
        # Working Capital Metrics
        ratios['working_capital'] = current_assets - current_liabilities
        ratios['working_capital_ratio'] = ratios['working_capital'] / total_revenue if total_revenue > 0 else 0
        ratios['cash_conversion_cycle'] = (ratios['days_inventory_outstanding'] + 
                                          ratios['days_sales_outstanding'] - 
                                          ratios['days_payables_outstanding'])
        
        # Cash Flow Ratios
        ratios['operating_cash_flow_ratio'] = operating_cash_flow / current_liabilities if current_liabilities > 0 else 0
        ratios['cash_flow_margin'] = (operating_cash_flow / total_revenue * 100) if total_revenue > 0 else 0
        
        return ratios
    
    def assess_creditworthiness(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, float],
        business_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess creditworthiness and assign credit rating
        
        Args:
            financial_data: Financial statement data
            ratios: Calculated financial ratios
            business_info: Business profile information
        
        Returns:
            Credit assessment including score and rating
        """
        score = 0
        max_score = 100
        
        # 1. Liquidity Assessment (20 points)
        current_ratio = ratios.get('current_ratio', 0)
        if current_ratio >= 2.0:
            score += 20
        elif current_ratio >= 1.5:
            score += 15
        elif current_ratio >= 1.0:
            score += 10
        else:
            score += 5
        
        # 2. Leverage Assessment (20 points)
        debt_to_equity = ratios.get('debt_to_equity', 0)
        if debt_to_equity <= 0.5:
            score += 20
        elif debt_to_equity <= 1.0:
            score += 15
        elif debt_to_equity <= 2.0:
            score += 10
        else:
            score += 5
        
        # 3. Profitability Assessment (25 points)
        net_margin = ratios.get('net_profit_margin', 0)
        if net_margin >= 15:
            score += 25
        elif net_margin >= 10:
            score += 20
        elif net_margin >= 5:
            score += 15
        elif net_margin >= 0:
            score += 10
        else:
            score += 0
        
        # 4. Cash Flow Assessment (20 points)
        operating_cf = financial_data.get('operating_cash_flow', 0)
        if operating_cf > 0:
            ocf_ratio = ratios.get('operating_cash_flow_ratio', 0)
            if ocf_ratio >= 0.4:
                score += 20
            elif ocf_ratio >= 0.2:
                score += 15
            else:
                score += 10
        else:
            score += 0
        
        # 5. Business Maturity (15 points)
        current_year = datetime.now().year
        established_year = business_info.get('established_year', current_year)
        years_in_business = current_year - established_year
        if years_in_business >= 10:
            score += 15
        elif years_in_business >= 5:
            score += 10
        elif years_in_business >= 2:
            score += 5
        else:
            score += 2
        
        # Determine credit rating
        credit_rating = self._score_to_rating(score)
        risk_level = self._score_to_risk(score)
        
        return {
            "creditworthiness_score": score,
            "credit_rating": credit_rating,
            "risk_level": risk_level,
            "score_breakdown": {
                "liquidity": min(20, score * 0.2),
                "leverage": min(20, score * 0.2),
                "profitability": min(25, score * 0.25),
                "cash_flow": min(20, score * 0.2),
                "maturity": min(15, score * 0.15)
            }
        }
    
    def _score_to_rating(self, score: float) -> str:
        """Convert numerical score to credit rating"""
        if score >= 90:
            return "AAA"
        elif score >= 80:
            return "AA"
        elif score >= 70:
            return "A"
        elif score >= 60:
            return "BBB"
        elif score >= 50:
            return "BB"
        elif score >= 40:
            return "B"
        elif score >= 30:
            return "CCC"
        elif score >= 20:
            return "CC"
        elif score >= 10:
            return "C"
        else:
            return "D"
    
    def _score_to_risk(self, score: float) -> str:
        """Convert numerical score to risk level"""
        if score >= 70:
            return "low"
        elif score >= 50:
            return "moderate"
        elif score >= 30:
            return "high"
        else:
            return "critical"
    
    def calculate_health_scores(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate various health scores
        
        Args:
            financial_data: Financial statement data
            ratios: Calculated financial ratios
        
        Returns:
            Dictionary of health scores
        """
        scores = {}
        
        # Liquidity Score (0-100)
        current_ratio = ratios.get('current_ratio', 0)
        quick_ratio = ratios.get('quick_ratio', 0)
        liquidity = min(100, (current_ratio * 30 + quick_ratio * 30 + 40))
        scores['liquidity_score'] = max(0, liquidity)
        
        # Profitability Score (0-100)
        net_margin = ratios.get('net_profit_margin', 0)
        roa = ratios.get('return_on_assets', 0)
        roe = ratios.get('return_on_equity', 0)
        profitability = (
            min(40, net_margin * 2) +
            min(30, roa * 1.5) +
            min(30, roe * 1.5)
        )
        scores['profitability_score'] = max(0, min(100, profitability))
        
        # Efficiency Score (0-100)
        asset_turnover = ratios.get('asset_turnover', 0)
        inventory_turnover = ratios.get('inventory_turnover', 0)
        efficiency = min(100, (asset_turnover * 40 + min(60, inventory_turnover * 10)))
        scores['efficiency_score'] = max(0, efficiency)
        
        # Overall Health Score (weighted average)
        scores['overall_health_score'] = (
            scores['liquidity_score'] * 0.30 +
            scores['profitability_score'] * 0.40 +
            scores['efficiency_score'] * 0.30
        )
        
        return scores
    
    def forecast_revenue(
        self,
        historical_data: List[Dict[str, Any]],
        periods: int = 3
    ) -> List[float]:
        """
        Forecast revenue using time series analysis
        
        Args:
            historical_data: List of historical financial data
            periods: Number of periods to forecast
        
        Returns:
            List of forecasted revenue values
        """
        if not historical_data or len(historical_data) < 3:
            return [0] * periods
        
        # Extract revenue values
        revenues = [data.get('total_revenue', 0) for data in historical_data]
        
        # Simple linear regression for trend
        x = np.arange(len(revenues))
        slope, intercept, _, _, _ = stats.linregress(x, revenues)
        
        # Forecast future periods
        forecasts = []
        for i in range(1, periods + 1):
            forecast = slope * (len(revenues) + i) + intercept
            # Ensure non-negative
            forecasts.append(max(0, forecast))
        
        return forecasts
    
    def analyze_cash_flow_pattern(
        self,
        transactions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze cash flow patterns from transactions
        
        Args:
            transactions: List of transaction records
        
        Returns:
            Cash flow analysis results
        """
        if not transactions:
            return {
                "average_monthly_inflow": 0,
                "average_monthly_outflow": 0,
                "volatility": 0,
                "trend": "stable"
            }
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(transactions)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['month'] = df['transaction_date'].dt.to_period('M')
        
        # Separate inflows and outflows
        inflows = df[df['amount'] > 0].groupby('month')['amount'].sum()
        outflows = df[df['amount'] < 0].groupby('month')['amount'].sum().abs()
        
        analysis = {
            "average_monthly_inflow": float(inflows.mean()) if len(inflows) > 0 else 0,
            "average_monthly_outflow": float(outflows.mean()) if len(outflows) > 0 else 0,
            "max_monthly_inflow": float(inflows.max()) if len(inflows) > 0 else 0,
            "min_monthly_inflow": float(inflows.min()) if len(inflows) > 0 else 0,
            "volatility": float(inflows.std()) if len(inflows) > 1 else 0,
            "trend": self._determine_trend(inflows.tolist() if len(inflows) > 0 else []),
            "months_analyzed": len(inflows)
        }
        
        return analysis
    
    def _determine_trend(self, values: List[float]) -> str:
        """Determine trend direction"""
        if len(values) < 2:
            return "stable"
        
        x = np.arange(len(values))
        slope, _, _, _, _ = stats.linregress(x, values)
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    def identify_cost_optimization_opportunities(
        self,
        financial_data: Dict[str, Any],
        industry_benchmarks: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Identify cost optimization opportunities
        
        Args:
            financial_data: Financial statement data
            industry_benchmarks: Industry comparison data
        
        Returns:
            List of cost optimization recommendations
        """
        opportunities = []
        
        total_revenue = financial_data.get('total_revenue', 0)
        if total_revenue == 0:
            return opportunities
        
        # Check operating expense ratio
        operating_expenses = financial_data.get('operating_expenses', 0)
        opex_ratio = (operating_expenses / total_revenue) * 100
        
        if opex_ratio > 30:
            opportunities.append({
                "area": "Operating Expenses",
                "current_percentage": round(opex_ratio, 2),
                "recommendation": "Operating expenses are high relative to revenue. Consider reviewing and optimizing operational costs.",
                "potential_savings": operating_expenses * 0.1  # Assume 10% reduction potential
            })
        
        # Check salary to revenue ratio
        salaries = financial_data.get('salaries_wages', 0)
        salary_ratio = (salaries / total_revenue) * 100
        
        if salary_ratio > 40:
            opportunities.append({
                "area": "Personnel Costs",
                "current_percentage": round(salary_ratio, 2),
                "recommendation": "Salary expenses are high. Consider workforce optimization or automation.",
                "potential_savings": salaries * 0.05
            })
        
        # Check inventory levels
        inventory = financial_data.get('inventory', 0)
        inventory_ratio = (inventory / total_revenue) * 100
        
        if inventory_ratio > 25:
            opportunities.append({
                "area": "Inventory Management",
                "current_percentage": round(inventory_ratio, 2),
                "recommendation": "Inventory levels are high. Implement just-in-time inventory management to reduce holding costs.",
                "potential_savings": inventory * 0.15
            })
        
        return opportunities
    
    def calculate_working_capital_metrics(
        self,
        financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate detailed working capital metrics
        
        Args:
            financial_data: Financial statement data
        
        Returns:
            Working capital analysis
        """
        current_assets = financial_data.get('current_assets', 0)
        current_liabilities = financial_data.get('current_liabilities', 0)
        total_revenue = financial_data.get('total_revenue', 0)
        
        working_capital = current_assets - current_liabilities
        
        return {
            "working_capital": working_capital,
            "working_capital_ratio": (working_capital / total_revenue) if total_revenue > 0 else 0,
            "current_ratio": current_assets / current_liabilities if current_liabilities > 0 else 0,
            "status": "healthy" if working_capital > 0 else "stressed",
            "adequacy": "adequate" if working_capital > (total_revenue * 0.1) else "insufficient"
        }


# Create singleton instance
financial_service = FinancialAnalysisService()
