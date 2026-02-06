# Financial Health Assessment Tool - Setup Guide

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker Desktop installed
- 8GB RAM minimum
- 10GB free disk space

### Step 1: Clone and Configure

```bash
cd "Financial Health Assessment"

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

### Step 2: Configure API Keys

Edit `.env` and add your API keys:

```env
# Required: Add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Optional: Claude API key
CLAUDE_API_KEY=your-claude-key-here

# Generate secure keys (run in terminal):
# For JWT_SECRET_KEY: openssl rand -hex 32
# For ENCRYPTION_KEY: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# For AES_ENCRYPTION_KEY: openssl rand -hex 32

JWT_SECRET_KEY=your-generated-jwt-secret-key
ENCRYPTION_KEY=your-generated-fernet-key
AES_ENCRYPTION_KEY=your-generated-aes-key
```

### Step 3: Launch Application

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

### Step 5: Create First User

1. Open http://localhost:3000
2. Click "Register" 
3. Fill in your details
4. Login with credentials

## Manual Installation (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp ../.env.example .env
# Edit .env with your configuration

# Start PostgreSQL (if not using Docker)
# Install PostgreSQL 14+ from https://www.postgresql.org/

# Create database
createdb financial_health_db

# Run migrations (when alembic is configured)
# alembic upgrade head

# Start backend server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

### Database Setup

```bash
# Install PostgreSQL 14+
# macOS: brew install postgresql@14
# Ubuntu: sudo apt install postgresql-14
# Windows: Download from postgresql.org

# Start PostgreSQL service
# macOS: brew services start postgresql@14
# Ubuntu: sudo systemctl start postgresql
# Windows: Use pgAdmin or services.msc

# Create database and user
psql -U postgres
CREATE DATABASE financial_health_db;
CREATE USER financialhealth WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE financial_health_db TO financialhealth;
\q
```

## Configuration Details

### Required API Keys

1. **OpenAI API Key**
   - Get from: https://platform.openai.com/api-keys
   - Required for AI-powered financial analysis
   - Cost: Pay-per-use (GPT-4 recommended)

2. **Claude API Key** (Optional)
   - Get from: https://console.anthropic.com/
   - Alternative to OpenAI
   - Configure via `AI_MODEL=claude-3-opus-20240229`

3. **Banking APIs** (Optional)
   - Plaid: https://plaid.com/
   - Razorpay: https://razorpay.com/

4. **GST API** (Optional)
   - Contact GST Network for API access
   - Required for GST return integration

### Security Keys Generation

```bash
# JWT Secret Key
openssl rand -hex 32

# Fernet Encryption Key (Python)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# AES Encryption Key
openssl rand -hex 32
```

## Testing the Installation

### 1. Backend Health Check

```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "database": "connected", "version": "1.0.0"}
```

### 2. Frontend Check

```bash
curl http://localhost:3000
# Should return HTML
```

### 3. API Documentation

Open http://localhost:8000/docs to see interactive API documentation

### 4. Test User Registration

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "SecurePassword123!",
    "company_name": "Test Company"
  }'
```

## Troubleshooting

### Database Connection Errors

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Backend Errors

```bash
# View backend logs
docker-compose logs backend

# Check environment variables
docker-compose exec backend env | grep DATABASE

# Restart backend
docker-compose restart backend
```

### Frontend Errors

```bash
# View frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose up --build frontend

# Clear node_modules and reinstall
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

## Production Deployment

### Environment Configuration

```env
# Production settings
ENVIRONMENT=production
DEBUG=False

# Use strong passwords
DATABASE_URL=postgresql://user:strong_password@db_host:5432/db_name

# Configure CORS for your domain
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### Security Checklist

- [ ] Change all default passwords
- [ ] Use HTTPS/TLS certificates
- [ ] Enable database encryption
- [ ] Configure firewall rules
- [ ] Set up regular backups
- [ ] Enable logging and monitoring
- [ ] Configure rate limiting
- [ ] Review and update API keys rotation policy

### Recommended Hosting

- **Backend**: AWS EC2, Google Cloud Run, DigitalOcean
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Database**: AWS RDS, Google Cloud SQL, managed PostgreSQL
- **File Storage**: AWS S3, Google Cloud Storage

## Development Workflow

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
black app/
flake8 app/

# Frontend linting
cd frontend
npm run lint
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Support

For issues and questions:
- Check documentation: README.md
- Review API docs: http://localhost:8000/docs
- Check logs: `docker-compose logs`

## Next Steps

1. ✅ Complete initial setup
2. Register your first user
3. Create a business profile
4. Upload sample financial data
5. Run your first assessment
6. Generate reports
7. Explore AI recommendations

Congratulations! Your Financial Health Assessment Tool is ready to use.
