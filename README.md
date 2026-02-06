# Financial Health Assessment Tool for SMEs

A comprehensive AI-powered financial health assessment platform for small and medium enterprises (SMEs) that analyzes financial statements, cash flow patterns, and business metrics to provide actionable insights and recommendations.

## Features

### Core Capabilities
- **AI-Powered Financial Analysis**: Leverages GPT/Claude for intelligent insights
- **Creditworthiness Evaluation**: Comprehensive credit scoring and risk assessment
- **Cash Flow Analysis**: Pattern recognition and forecasting
- **Cost Optimization**: AI-driven recommendations for expense reduction
- **Financial Product Recommendations**: Suitable products from banks and NBFCs
- **Automated Bookkeeping Assistance**: Streamline accounting processes
- **Tax Compliance Checking**: Ensure regulatory adherence
- **Financial Forecasting**: Predictive analytics for business planning
- **Working Capital Optimization**: Maximize operational efficiency

### Advanced Features
- **Industry Benchmarking**: Compare against industry-specific metrics
- **Multi-business Type Support**: Manufacturing, Retail, Agriculture, Services, Logistics, E-commerce
- **GST Integration**: Import and analyze GST returns
- **Banking API Integration**: Real-time financial data sync
- **Investor-Ready Reports**: Professional financial reports for stakeholders
- **Multilingual Support**: English + Hindi/Regional languages
- **Interactive Dashboards**: Visual representation of financial metrics

### Security & Compliance
- End-to-end encryption for data at rest and in transit
- GDPR/SOC2 compliant architecture
- Secure authentication and authorization
- Audit logs for all financial operations

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with encryption
- **AI/LLM**: OpenAI GPT-4/Claude
- **Data Processing**: pandas, NumPy, scikit-learn
- **Security**: cryptography, bcrypt, JWT

### Frontend
- **Framework**: React.js with TypeScript
- **UI Library**: Material-UI (MUI)
- **Charts**: Recharts, Chart.js
- **State Management**: Redux Toolkit
- **i18n**: react-i18next

### Integrations
- Banking APIs (max 2): Plaid, Razorpay
- GST API integration
- Payment gateway integration

## Project Structure

```
financial-health-assessment/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── ai_analysis.py
│   │   │   ├── financial_analysis.py
│   │   │   ├── risk_assessment.py
│   │   │   └── integrations/
│   │   └── utils/
│   ├── alembic/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── locales/
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 14+
- Docker (optional)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example .env
# Edit .env with your configuration

# Initialize database
alembic upgrade head

# Run the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API endpoint

# Run the development server
npm start
```

### Docker Setup (Recommended)

```bash
docker-compose up --build
```

## Configuration

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/financial_health
DATABASE_ENCRYPTION_KEY=your-encryption-key-here

# API Keys
OPENAI_API_KEY=your-openai-api-key
CLAUDE_API_KEY=your-claude-api-key

# Banking APIs
PLAID_CLIENT_ID=your-plaid-client-id
PLAID_SECRET=your-plaid-secret
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

# GST API
GST_API_KEY=your-gst-api-key
GST_API_URL=https://gst-api-url

# Security
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## Usage

### 1. Upload Financial Data
- Upload CSV/XLSX/PDF financial statements
- Connect banking APIs for real-time data
- Import GST returns

### 2. AI Analysis
- System automatically analyzes financial health
- Generates credit scores and risk assessments
- Provides actionable recommendations

### 3. View Reports
- Interactive dashboards with financial metrics
- Download investor-ready reports
- Export data in multiple formats

### 4. Get Recommendations
- Cost optimization strategies
- Suitable financial products
- Tax planning suggestions
- Working capital improvements

## API Documentation

Once the backend is running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Security Features

- **Data Encryption**: AES-256 encryption for data at rest
- **TLS/SSL**: All data in transit encrypted
- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control (RBAC)
- **Audit Logs**: Complete audit trail for all operations
- **Data Anonymization**: PII data anonymized where appropriate

## Multilingual Support

Currently supported languages:
- English (en)
- Hindi (hi)
- Additional regional languages can be added via i18n configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For support, email support@financialhealth.com or create an issue in the repository.

## Roadmap

- [ ] Integration with additional banking APIs
- [ ] Machine learning models for enhanced predictions
- [ ] Mobile application (React Native)
- [ ] Advanced fraud detection
- [ ] Blockchain integration for audit trails
- [ ] More regional language support
