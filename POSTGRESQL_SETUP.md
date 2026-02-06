# PostgreSQL Setup Guide

## Current Status
PostgreSQL@18 is being installed via Homebrew (installation in progress).

## Step-by-Step Setup (Run these after installation completes)

### Step 1: Start PostgreSQL Service

```bash
# Start PostgreSQL
brew services start postgresql@18

# Or start without brew services:
/Users/vivek4/homebrew/opt/postgresql@18/bin/postgres -D /Users/vivek4/homebrew/var/postgresql@18
```

### Step 2: Add PostgreSQL to PATH

```bash
echo 'export PATH="/Users/vivek4/homebrew/opt/postgresql@18/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Create Database and User

```bash
# Connect to PostgreSQL as default user
psql postgres

# Then run these SQL commands:
CREATE DATABASE financial_health_db;
CREATE USER financialhealth WITH PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE financial_health_db TO financialhealth;
\q
```

### Step 4: Update Backend .env File

Edit `/Users/vivek4/Documents/Financial Health Assessment/backend/.env`:

```env
# Replace this line:
DATABASE_URL=sqlite:///./financial_health.db

# With this:
DATABASE_URL=postgresql://financialhealth:your_secure_password_here@localhost:5432/financial_health_db
```

### Step 5: Restart Backend Server

```bash
# If backend is running, stop it (Ctrl+C)
# Then restart:
cd "/Users/vivek4/Documents/Financial Health Assessment/backend"
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Quick One-Liner Setup

Once PostgreSQL is installed, run this:

```bash
# Start PostgreSQL
brew services start postgresql@18

# Create database and user
psql postgres -c "CREATE DATABASE financial_health_db;"
psql postgres -c "CREATE USER financialhealth WITH PASSWORD 'SecureDBPass2026!';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE financial_health_db TO financialhealth;"
psql postgres -c "ALTER DATABASE financial_health_db OWNER TO financialhealth;"

echo "✅ PostgreSQL setup complete!"
```

Then update backend/.env:
```env
DATABASE_URL=postgresql://financialhealth:SecureDBPass2026!@localhost:5432/financial_health_db
```

---

## Verify Installation

```bash
# Check PostgreSQL version
psql --version

# Check if service is running
brew services list | grep postgresql

# List databases
psql postgres -c "\l"

# Connect to your database
psql financial_health_db
```

---

## Troubleshooting

### PostgreSQL won't start

```bash
# Check logs
brew services info postgresql@18

# Or manually check:
tail -f /Users/vivek4/homebrew/var/log/postgresql@18.log
```

### Connection refused

```bash
# Ensure PostgreSQL is running
ps aux | grep postgres

# Restart service
brew services restart postgresql@18
```

### Permission denied

```bash
# Fix permissions
chmod 700 /Users/vivek4/homebrew/var/postgresql@18
```

---

## Migration from SQLite to PostgreSQL

Your current SQLite database will remain at `backend/financial_health.db`. When you switch to PostgreSQL:

1. New database will be empty
2. You'll need to register users again
3. Or export/import data from SQLite to PostgreSQL

---

## Benefits of PostgreSQL vs SQLite

✅ **Better concurrency** - Multiple users simultaneously  
✅ **Production-ready** - Enterprise-grade reliability  
✅ **Advanced features** - Full ACID compliance  
✅ **Better performance** - For large datasets  
✅ **Scalability** - Handles growth better  
✅ **Security** - Row-level security, encryption at rest  

---

## Wait Time

PostgreSQL installation typically takes **2-5 minutes** depending on your system.

Once you see:
```
==> postgresql@18 installed successfully!
```

Run the setup commands above to configure it!
