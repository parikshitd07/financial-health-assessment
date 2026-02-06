# API Documentation

## Base URL
`http://localhost:8000/api/v1`

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "password": "SecurePassword123!",
  "company_name": "Company Name",
  "industry": "retail",
  "phone": "+91-9876543210"
}

Response: 201 Created
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "role": "business_owner",
  "is_active": true,
  "created_at": "2026-05-02T16:30:00"
}
```

#### Login
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=username&password=SecurePassword123!

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "company_name": "Company Name",
  "role": "business_owner"
}
```

### Business Management

#### Create Business
```http
POST /business/
Authorization: Bearer <token>
Content-Type: application/json

{
  "business_name": "ABC Retail Store",
  "industry": "retail",
  "gst_number": "27AAAAA0000A1Z5",
  "pan_number": "AAAAA0000A",
  "annual_revenue": 5000000,
  "employee_count": 25,
  "city": "Mumbai",
  "state": "Maharashtra"
}
```

#### Get Businesses
```http
GET /business/
Authorization: Bearer <token>

Response: 200 OK
[
  {
    "id": 1,
    "business_name": "ABC Retail Store",
    "industry": "retail",
    "annual_revenue": 5000000
  }
]
```

### Financial Data

#### Upload Financial Data
```http
POST /financial-data/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <financial_statement.csv>
business_id: 1
fiscal_year: 2024

Response: 201 Created
{
  "id": 1,
  "business_id": 1,
  "total_revenue": 5000000,
  "total_expenses": 3500000,
  "fiscal_year": 2024
}
```

#### Get Financial Data
```http
GET /financial-data/?business_id=1&fiscal_year=2024
Authorization: Bearer <token>

Response: 200 OK
[
  {
    "id": 1,
    "total_revenue": 5000000,
    "total_expenses": 3500000,
    "total_assets": 2000000,
    "total_liabilities": 800000
  }
]
```

### Financial Assessment

#### Generate Assessment
```http
POST /assessment/{business_id}
Authorization: Bearer <token>

Response: 201 Created
{
  "id": 1,
  "business_id": 1,
  "overall_health_score": 75,
  "creditworthiness_score": 72,
  "credit_rating": "A",
  "risk_level": "low",
  "ai_summary": "Your business shows strong financial health...",
  "strengths": [
    "Healthy profit margins",
    "Strong liquidity position"
  ],
  "recommended_products": [
    {
      "product_type": "working_capital_loan",
      "provider": "HDFC Bank",
      "amount": 500000,
      "reason": "To expand inventory"
    }
  ]
}
```

#### Get Assessment
```http
GET /assessment/{assessment_id}
Authorization: Bearer <token>

Response: 200 OK
{
  "id": 1,
  "overall_health_score": 75,
  "ai_summary": "...",
  "recommendations": {...}
}
```

### Reports

#### Generate Report
```http
POST /reports/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "assessment_id": 1,
  "report_type": "investor",
  "language": "en"
}

Response: 201 Created
{
  "id": 1,
  "report_name": "Financial Health Report - Q4 2024",
  "report_type": "investor",
  "pdf_path": "/reports/report_1.pdf",
  "generated_at": "2026-05-02T16:30:00"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "An internal server error occurred"
}
```

## Rate Limiting

- 60 requests per minute per IP
- 1000 requests per hour per IP

## Data Models

### User
- id: integer
- email: string
- username: string
- full_name: string
- company_name: string (optional)
- industry: string (optional)
- role: enum (admin, business_owner, accountant, viewer)

### Business
- id: integer
- business_name: string
- industry: enum
- gst_number: string
- annual_revenue: float
- employee_count: integer

### FinancialAssessment
- id: integer
- overall_health_score: float (0-100)
- creditworthiness_score: float (0-100)
- credit_rating: enum (AAA, AA, A, BBB, BB, B, CCC, CC, C, D)
- risk_level: enum (low, moderate, high, critical)
- ai_summary: text
- recommendations: JSON

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation with the ability to test endpoints directly.
