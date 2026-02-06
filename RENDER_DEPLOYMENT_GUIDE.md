# 🚀 Deploying to Render with PostgreSQL

Complete guide for deploying your Financial Health Assessment platform to Render.com with managed PostgreSQL database.

## 📋 Prerequisites

- Render.com account (free tier available)
- GitHub repository with your code
- Your application is already PostgreSQL-ready! ✅

## 🗄️ Step 1: Create PostgreSQL Database on Render

### 1.1 Create Database
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `financial-health-db`
   - **Database**: `financial_health`
   - **User**: `financial_health_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)
4. Click **"Create Database"**

### 1.2 Get Database Connection String
After creation, Render provides:
- **Internal Database URL**: `postgresql://user:pass@host:5432/dbname`
- **External Database URL**: For external connections
- **PSQL Command**: For direct access

**Copy the Internal Database URL** - you'll need it!

Example:
```
postgresql://financial_health_user:abc123xyz@dpg-xxxxx-a.oregon-postgres.render.com/financial_health
```

## 🔧 Step 2: Prepare Your Application

### 2.1 Your App is Already Ready!
✅ **psycopg2-binary** already in requirements.txt
✅ **SQLAlchemy** configured to use DATABASE_URL
✅ **Models** work with both SQLite and PostgreSQL

### 2.2 Update .env (Local Testing Only)
For local testing with PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/financial_health
```

**Note**: Don't commit .env to GitHub!

## 🚀 Step 3: Deploy Backend to Render

### 3.1 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `financial-health-backend`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3.2 Add Environment Variables
In the **Environment** section, add:

```env
# Database (use Internal Database URL from Step 1.2)
DATABASE_URL=postgresql://financial_health_user:abc123xyz@dpg-xxxxx-a.oregon-postgres.render.com/financial_health
DATABASE_ENCRYPTION_KEY=your-32-char-encryption-key-here

# AI/LLM
GEMINI_API_KEY=your-gemini-api-key
AI_MODEL=gemini-3-flash-preview
GEMINI_THINKING_LEVEL=medium

# Security
JWT_SECRET_KEY=your-production-jwt-secret-key-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Encryption
ENCRYPTION_KEY=your-base64-encryption-key
AES_ENCRYPTION_KEY=your-32-char-aes-key

# Application
APP_NAME=Financial Health Assessment Tool
APP_VERSION=1.0.0
DEBUG=False
ENVIRONMENT=production

# File Upload
MAX_UPLOAD_SIZE_MB=50
UPLOAD_FOLDER=./uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

### 3.3 Deploy
1. Click **"Create Web Service"**
2. Render will:
   - Clone your repo
   - Install dependencies
   - Start your app
   - Provide a URL: `https://financial-health-backend.onrender.com`

## 🌐 Step 4: Deploy Frontend to Render

### 4.1 Create Static Site
1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `financial-health-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`

### 4.2 Update Frontend API URL
Before deploying, update your frontend to use the backend URL:

**frontend/src/config.ts** (create if doesn't exist):
```typescript
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

**Add environment variable in Render:**
```env
REACT_APP_API_URL=https://financial-health-backend.onrender.com
```

### 4.3 Update CORS in Backend
Add your frontend URL to CORS origins in backend `.env`:
```env
CORS_ORIGINS=https://financial-health-frontend.onrender.com,http://localhost:3000
```

## 🗄️ Step 5: Initialize Database

### 5.1 Connect to Database
Use Render's PSQL command or any PostgreSQL client:
```bash
psql postgresql://financial_health_user:abc123xyz@dpg-xxxxx-a.oregon-postgres.render.com/financial_health
```

### 5.2 Tables Auto-Created
Your app automatically creates tables on first run via:
```python
Base.metadata.create_all(bind=engine)
```

### 5.3 Verify Tables
```sql
\dt  -- List all tables
SELECT * FROM users LIMIT 5;
SELECT * FROM businesses LIMIT 5;
SELECT * FROM assessments LIMIT 5;
```

## 📊 Step 6: Database Management

### 6.1 Access Database
**Via Render Dashboard:**
- Go to your PostgreSQL service
- Click **"Connect"** → **"External Connection"**
- Use provided credentials

**Via pgAdmin:**
1. Download [pgAdmin](https://www.pgadmin.org/)
2. Add new server with Render's external connection details

**Via Command Line:**
```bash
psql <EXTERNAL_DATABASE_URL>
```

### 6.2 Backup Database
**Automatic Backups:**
- Render provides automatic daily backups (paid plans)
- Free tier: Manual backups only

**Manual Backup:**
```bash
pg_dump <DATABASE_URL> > backup.sql
```

**Restore Backup:**
```bash
psql <DATABASE_URL> < backup.sql
```

### 6.3 Database Migrations
For schema changes, use Alembic:

**Install Alembic:**
```bash
pip install alembic
alembic init alembic
```

**Create Migration:**
```bash
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

## 🔒 Security Best Practices

### 1. Environment Variables
- ✅ Never commit .env to GitHub
- ✅ Use Render's environment variables
- ✅ Rotate secrets regularly

### 2. Database Security
- ✅ Use strong passwords
- ✅ Enable SSL (Render does this automatically)
- ✅ Restrict access to internal network

### 3. API Security
- ✅ Enable HTTPS (Render provides free SSL)
- ✅ Set DEBUG=False in production
- ✅ Implement rate limiting

## 📈 Monitoring & Logs

### View Logs
**Backend Logs:**
- Render Dashboard → Your service → **Logs** tab
- Real-time streaming logs

**Database Logs:**
- PostgreSQL service → **Logs** tab

### Metrics
- Render provides:
  - CPU usage
  - Memory usage
  - Request count
  - Response times

## 💰 Pricing

### Free Tier
- **Web Service**: 750 hours/month (sleeps after 15 min inactivity)
- **PostgreSQL**: 90 days free, then $7/month
- **Static Site**: Free forever

### Paid Plans
- **Starter**: $7/month (always on)
- **Standard**: $25/month (more resources)
- **Pro**: $85/month (high performance)

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push
Render automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render will:
1. Detect changes
2. Build application
3. Deploy automatically
4. Zero downtime deployment

## 🆘 Troubleshooting

### Database Connection Issues
```python
# Test connection
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
connection = engine.connect()
print("Connected!")
```

### Migration Issues
```bash
# Reset database (CAUTION: Deletes all data!)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

### App Not Starting
- Check logs in Render dashboard
- Verify all environment variables
- Ensure requirements.txt is complete

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [PostgreSQL on Render](https://render.com/docs/databases)
- [Deploy FastAPI](https://render.com/docs/deploy-fastapi)
- [Environment Variables](https://render.com/docs/environment-variables)

## ✅ Deployment Checklist

- [ ] Create PostgreSQL database on Render
- [ ] Copy Internal Database URL
- [ ] Create backend web service
- [ ] Add all environment variables
- [ ] Deploy backend
- [ ] Test backend API
- [ ] Create frontend static site
- [ ] Update API URL in frontend
- [ ] Deploy frontend
- [ ] Update CORS settings
- [ ] Test full application
- [ ] Set up database backups
- [ ] Monitor logs and metrics

## 🎉 Your App is Live!

**Backend**: `https://financial-health-backend.onrender.com`
**Frontend**: `https://financial-health-frontend.onrender.com`
**Database**: Managed PostgreSQL on Render

**Your Financial Health Assessment platform is now production-ready with PostgreSQL!** 🚀
