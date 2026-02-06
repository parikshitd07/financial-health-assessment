# Sample Financial Data Files

This folder contains ready-to-use sample financial documents for testing the Financial Health Assessment Tool.

---

## 📁 Files Included

### 1. **sample_balance_sheet.csv**
Sample balance sheet for a manufacturing SME with ₹6.2M in assets.

**Contains:**
- Current Assets: ₹1.6M (Cash, Receivables, Inventory)
- Fixed Assets: ₹4.6M (Land, Building, Machinery, Vehicles)
- Total Liabilities: ₹2.83M
- Equity: ₹3.37M

**Financial Health Indicators:**
- Current Ratio: ~3.0 (Healthy)
- Debt-to-Equity: ~0.84 (Moderate)

---

### 2. **sample_profit_loss.csv**
Sample P&L statement for FY 2024 showing profitable operations.

**Contains:**
- Total Revenue: ₹2.55M
- Total Expenses: ₹2.17M
- Net Profit: ₹380K (before taxes)
- Tax Paid: ₹310K

**Performance Indicators:**
- Gross Margin: ~56%
- Net Margin: ~15%
- COGS Ratio: 43%

---

### 3. **sample_cash_flow.csv**
Sample cash flow statement showing positive cash generation.

**Contains:**
- Operating Cash Flow: +₹555K
- Investing Cash Flow: -₹300K
- Financing Cash Flow: +₹330K
- Net Cash Flow: +₹585K

**Cash Health:**
- Positive operating cash flow
- Strategic investments
- Healthy financing

---

## 🚀 How to Use These Files

### Method 1: Upload via Web Interface
1. Go to http://localhost:3000/financial-data
2. Click "Upload Financial Data"
3. Select one or more sample CSV files
4. Submit

### Method 2: Test via API
```bash
curl -X POST "http://localhost:8000/api/v1/financial-data/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_balance_sheet.csv" \
  -F "fiscal_year=2024"
```

### Method 3: View/Edit in Excel
1. Open any CSV file in Excel
2. Modify amounts to match your business
3. Save and upload

---

## 📊 Expected Analysis Results

When you upload these files, the AI will analyze and provide:

### Financial Ratios
- **Current Ratio**: 3.0 (Excellent liquidity)
- **Quick Ratio**: 2.3 (Strong)
- **Debt-to-Equity**: 0.84 (Moderate leverage)
- **ROA**: ~6% (Return on Assets)
- **Gross Margin**: 56% (Healthy)
- **Net Margin**: 15% (Good profitability)

### Health Scores
- **Overall Health**: 75-80/100
- **Creditworthiness**: 70-75/100
- **Liquidity**: 85-90/100
- **Profitability**: 70-75/100

### Credit Rating
- Expected: **A** or **BBB**
- Risk Level: **Low** to **Moderate**

### AI Recommendations
- Working capital is strong
- Consider reducing debt slightly
- Operating expenses are within normal range
- Cash flow is healthy
- Good time for strategic investments

---

## 🎯 Customize for Your Business

### Quick Customization:
1. Open CSV files in Excel/Numbers
2. Change amounts to match your business
3. Keep the Category and Item columns
4. Save as CSV
5. Upload!

### Example: Retail Business
```csv
Category,Item,Amount
Assets,Cash and Bank,300000
Assets,Inventory,800000
Assets,Store Equipment,400000
Liabilities,Accounts Payable,200000
Equity,Owner's Capital,1300000
```

### Example: Service Business
```csv
Category,Item,Amount
Revenue,Consulting Services,1500000
Revenue,Training Services,500000
Expenses,Employee Salaries,800000
Expenses,Office Rent,200000
Expenses,Marketing,100000
```

---

## 📈 Understanding the Numbers

### Balance Sheet Rules:
```
Total Assets = Total Liabilities + Total Equity
```

In our sample:
- Assets: ₹6.2M
- Liabilities: ₹2.83M
- Equity: ₹3.37M
- Balanced: ✅ (₹6.2M = ₹2.83M + ₹3.37M)

### P&L Rules:
```
Net Profit = Total Revenue - Total Expenses
```

In our sample:
- Revenue: ₹2.55M
- Expenses: ₹2.17M
- Net Profit: ₹380K
- Profitable: ✅

---

## 💡 Tips for Real Data

### What to Include:
✅ Actual numbers from your accounting software
✅ Latest completed fiscal year
✅ All revenue streams
✅ All expense categories
✅ Accurate asset valuations
✅ All outstanding debts

### What to Avoid:
❌ Estimated or guessed numbers
❌ Incomplete data
❌ Mixed currencies
❌ Duplicate entries

---

## 🔍 File Format Requirements

**Accepted Formats:**
- CSV (.csv) - **Recommended**
- Excel (.xlsx)
- PDF (text-based only)

**File Size:**
- Maximum: 50MB per file
- Recommended: Under 5MB

**Encoding:**
- UTF-8 (for special characters)

---

## ✨ Next Steps

1. **Test with samples**: Upload the provided files
2. **View analysis**: See AI-generated insights
3. **Get recommendations**: Review cost optimization tips
4. **Replace with your data**: Use your actual financial figures
5. **Generate reports**: Create investor-ready reports

---

## 📞 Need Help?

See **FINANCIAL_DOCUMENTS_GUIDE.md** for:
- Detailed document descriptions
- Industry-specific guidance
- Advanced formatting tips
- Export instructions from accounting software

---

**Ready to test? Upload these sample files from your dashboard!**
