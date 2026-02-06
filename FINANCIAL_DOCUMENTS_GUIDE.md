# Financial Documents Guide

## What to Upload to Financial Health Assessment Tool

---

## 📊 Required Financial Documents

### 1. **Balance Sheet** (Most Important)
Shows your company's financial position at a specific date.

**What it includes:**
- **Assets**:
  - Current Assets (Cash, Bank balance, Receivables, Inventory)
  - Fixed Assets (Property, Equipment, Vehicles)
  
- **Liabilities**:
  - Current Liabilities (Accounts Payable, Short-term loans)
  - Long-term Liabilities (Long-term debt, Mortgages)
  
- **Equity**:
  - Owner's equity
  - Retained earnings

**Format**: Excel (.xlsx), CSV (.csv), or PDF

---

### 2. **Profit & Loss Statement (P&L)**
Shows revenues and expenses over a period (monthly/quarterly/yearly).

**What it includes:**
- **Revenue/Sales**: Total income from business operations
- **Cost of Goods Sold (COGS)**: Direct costs of producing goods/services
- **Gross Profit**: Revenue minus COGS
- **Operating Expenses**:
  - Salaries & wages
  - Rent
  - Utilities
  - Marketing
  - Insurance
  - Other expenses
- **Net Profit**: Final profit after all expenses

**Format**: Excel (.xlsx), CSV (.csv), or PDF

---

### 3. **Cash Flow Statement**
Shows how cash moves in and out of your business.

**What it includes:**
- **Operating Activities**: Cash from day-to-day business
- **Investing Activities**: Cash from buying/selling assets
- **Financing Activities**: Cash from loans/investments

**Format**: Excel (.xlsx), CSV (.csv), or PDF

---

### 4. **Bank Statements** (Optional but Recommended)
Shows actual cash transactions and balances.

**What it includes:**
- Opening balance
- All deposits
- All withdrawals
- Closing balance
- Transaction details

**Format**: PDF or CSV from your bank

---

### 5. **GST Returns** (For Indian Businesses)
Tax compliance and revenue verification.

**What it includes:**
- GSTR-1: Outward supplies
- GSTR-3B: Summary return
- GST collected
- GST paid

**Format**: PDF or JSON from GST portal

---

## 📑 Sample CSV Format (Balance Sheet)

Create a file named `balance_sheet_2024.csv`:

```csv
Category,Item,Amount
Assets,Cash and Bank,500000
Assets,Accounts Receivable,300000
Assets,Inventory,200000
Assets,Fixed Assets,1000000
Liabilities,Accounts Payable,150000
Liabilities,Short-term Debt,100000
Liabilities,Long-term Debt,400000
Equity,Owner's Equity,1350000
```

---

## 📑 Sample CSV Format (Profit & Loss)

Create a file named `profit_loss_2024.csv`:

```csv
Category,Item,Amount
Revenue,Product Sales,2000000
Revenue,Service Revenue,500000
Expenses,Cost of Goods Sold,1000000
Expenses,Salaries,400000
Expenses,Rent,120000
Expenses,Utilities,30000
Expenses,Marketing,50000
Expenses,Insurance,20000
Expenses,Other Expenses,80000
Taxes,Income Tax,100000
Taxes,GST Paid,180000
```

---

## 📑 Sample CSV Format (Cash Flow)

Create a file named `cash_flow_2024.csv`:

```csv
Category,Description,Amount
Operating,Cash from Sales,2300000
Operating,Payments to Suppliers,-980000
Operating,Salary Payments,-400000
Operating,Other Operating Expenses,-200000
Investing,Equipment Purchase,-150000
Investing,Vehicle Sale,80000
Financing,Loan Received,200000
Financing,Loan Repayment,-120000
```

---

## 📑 Sample Excel Template Structure

### Sheet 1: Company Information
```
Business Name: ABC Manufacturing Ltd
GST Number: 27AAAAA0000A1Z5
PAN Number: AAAAA0000A
Industry: Manufacturing
Fiscal Year: 2024
Period: April 2024 - March 2025
```

### Sheet 2: Balance Sheet
```
Assets          | Amount (₹)
----------------------------------------
Current Assets
  Cash          | 500,000
  Bank          | 1,200,000
  Receivables   | 800,000
  Inventory     | 1,000,000
Total Current   | 3,500,000

Fixed Assets
  Land          | 2,000,000
  Building      | 3,000,000
  Equipment     | 1,500,000
Total Fixed     | 6,500,000

TOTAL ASSETS    | 10,000,000

Liabilities
Current
  Payables      | 600,000
  Short-term Debt| 400,000
Total Current   | 1,000,000

Long-term
  Loans         | 3,000,000

TOTAL LIABILITIES| 4,000,000

Equity          | 6,000,000
```

---

## 🎯 What the Tool Analyzes

Once you upload these documents, the AI will analyze:

### Financial Ratios
- Current Ratio (liquidity)
- Quick Ratio
- Debt-to-Equity Ratio
- Return on Assets (ROA)
- Return on Equity (ROE)
- Gross Profit Margin
- Net Profit Margin
- Asset Turnover
- Inventory Turnover

### Health Scores
- Overall Financial Health (0-100)
- Creditworthiness Score
- Liquidity Score
- Profitability Score
- Efficiency Score

### Assessments
- Credit Rating (AAA to D)
- Risk Level (Low/Moderate/High/Critical)
- Working Capital status
- Cash Conversion Cycle

### AI Recommendations
- Cost optimization opportunities
- Revenue enhancement strategies
- Working capital improvements
- Tax optimization tips
- Suitable financial products
- Risk mitigation strategies

---

## 📝 Document Preparation Tips

### For CSV Files:
1. Use simple column headers
2. One row per line item
3. Numbers without currency symbols
4. Save as UTF-8 encoding

### For Excel Files:
1. Keep it simple - avoid complex formulas
2. One sheet per financial statement
3. Clear headers in first row
4. Numbers in standard format

### For PDF Files:
1. Must be **text-based** (not scanned images)
2. Clear, readable formatting
3. Table structures preferred
4. Searchable text

---

## 💡 Quick Start - Create Sample Data

### Option 1: Use Provided Samples
Copy the CSV examples above into files and upload them!

### Option 2: Export from Accounting Software
If you use:
- **Tally**: Export to Excel
- **QuickBooks**: Export reports to CSV
- **Zoho Books**: Download financial statements
- **Excel**: Save your existing sheets

### Option 3: Manual Entry
Create a simple Excel with your business numbers following the template above.

---

## 🔍 What File Format is Best?

### Recommended Order:
1. **CSV** (Best) - Easy to parse, no formatting issues
2. **Excel (.xlsx)** (Good) - Can include multiple sheets
3. **PDF** (Ok) - Must be text-based, not scanned

---

## 📊 Minimum Data Required

To get a basic assessment, you need at least:

### Essential:
- Total Revenue
- Total Expenses
- Total Assets
- Total Liabilities

### Recommended:
- Cash balance
- Accounts Receivable
- Accounts Payable
- Inventory (if applicable)

### Ideal:
- All balance sheet items
- Detailed P&L
- Cash flow statement
- 12 months of data

---

## 🎯 Industry-Specific Documents

### Retail:
- Inventory turnover reports
- Sales by product category
- Daily/weekly sales reports

### Manufacturing:
- Production costs
- Raw material inventory
- Work-in-progress inventory

### Services:
- Billable hours
- Project-wise revenue
- Resource utilization

### E-commerce:
- Platform fees
- Shipping costs
- Returns/refunds data

---

## ✅ Sample Data Files Included

I'll create sample files for you to test:

1. `sample_balance_sheet.csv`
2. `sample_profit_loss.csv`
3. `sample_cash_flow.csv`

You can upload these to see how the system works!

---

## 📌 Quick Summary

**Upload any of these:**
- Balance Sheet (Assets, Liabilities, Equity)
- Profit & Loss Statement (Revenue, Expenses)
- Cash Flow Statement
- Bank Statements
- GST Returns (Indian businesses)

**Formats accepted:**
- CSV (.csv)
- Excel (.xlsx)
- PDF (text-based)

**The tool will:**
- Analyze your financial health
- Generate scores and ratings
- Provide AI recommendations
- Create professional reports

---

Ready to test? I can create sample files for you!
