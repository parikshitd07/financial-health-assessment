# pgAdmin 4 - PostgreSQL UI Guide

## What is pgAdmin?

pgAdmin is a visual management tool for PostgreSQL that allows you to:
- ✅ View and manage databases visually
- ✅ Browse tables and data
- ✅ Run SQL queries with syntax highlighting
- ✅ Create databases without command line
- ✅ Monitor database performance
- ✅ Import/export data easily

---

## After Installation Completes

### Step 1: Launch pgAdmin 4

```bash
# Open pgAdmin from Applications
open /Applications/pgAdmin\ 4.app

# Or search for "pgAdmin 4" in Spotlight (Cmd+Space)
```

### Step 2: Set Master Password

First time you open pgAdmin, it will ask for a **master password** to secure your database connections.

- Choose a strong password
- This is NOT your database password
- You'll need this to unlock pgAdmin each time

### Step 3: Add PostgreSQL Server Connection

Once pgAdmin opens:

1. **Right-click** on "Servers" in the left panel
2. Click **"Register" → "Server..."**
3. Fill in the details:

**General Tab:**
- Name: `Financial Health DB`

**Connection Tab:**
- Host: `localhost`
- Port: `5432`
- Maintenance database: `postgres`
- Username: `financialhealth`
- Password: `SecureDBPass2026!` (or the password you set)
- ✅ Check "Save password"

4. Click **"Save"**

---

## Using pgAdmin to Create Database

### Method 1: Visual Creation

1. Expand "Servers" → "Financial Health DB"
2. Right-click on "Databases"
3. Click "Create" → "Database..."
4. Enter name: `financial_health_db`
5. Owner: `financialhealth`
6. Click "Save"

### Method 2: Using Query Tool

1. Right-click on "Servers" → "Financial Health DB"
2. Click "Query Tool"
3. Paste this SQL:

```sql
CREATE DATABASE financial_health_db;
GRANT ALL PRIVILEGES ON DATABASE financial_health_db TO financialhealth;
```

4. Click the ▶️ (Execute) button

---

## Viewing Your Application Data

### After Backend Creates Tables:

1. Expand `financial_health_db` → `Schemas` → `public` → `Tables`
2. You'll see:
   - `users` - Registered users
   - `businesses` - Business profiles  
   - `financial_data` - Financial statements
   - `financial_assessments` - AI assessments
   - `transactions` - Transaction records
   - `financial_reports` - Generated reports

### View User Data:

1. Right-click on `users` table
2. Click "View/Edit Data" → "All Rows"
3. See all registered users!

---

## Useful pgAdmin Features

### 1. Run SQL Queries

```sql
-- See all registered users
SELECT id, username, email, full_name, company_name, created_at
FROM users;

-- Count total users
SELECT COUNT(*) FROM users;

-- Find a specific user
SELECT * FROM users WHERE email = 'test@example.com';
```

### 2. Export Data

1. Right-click on table
2. Click "Import/Export Data"
3. Choose format (CSV, Excel, etc.)
4. Download your data!

### 3. Backup Database

1. Right-click on `financial_health_db`
2. Click "Backup..."
3. Choose location and format
4. Creates a backup file

### 4. Monitor Performance

- Click on "Dashboard" to see:
  - Active connections
  - Database size
  - Query performance
  - Server statistics

---

## Alternative PostgreSQL UI Tools

If you prefer other tools:

### 1. **TablePlus** (Premium, but beautiful)
```bash
brew install --cask tableplus
```
- Modern, fast interface
- Supports multiple databases
- Free trial available

### 2. **Postico** (Mac-native, clean)
```bash
brew install --cask postico
```
- Simple, elegant design
- Mac-optimized
- Free version available

### 3. **DBeaver** (Free, powerful)
```bash
brew install --cask dbeaver-community
```
- Feature-rich
- Supports many databases
- Completely free

### 4. **DataGrip** (Professional, JetBrains)
- Part of JetBrains suite
- Very powerful
- Paid (30-day trial)

---

## Connecting Your App to PostgreSQL

### After pgAdmin Setup:

1. **Ensure PostgreSQL is running**:
   ```bash
   brew services start postgresql@18
   ```

2. **Update backend/.env**:
   ```env
   DATABASE_URL=postgresql://financialhealth:SecureDBPass2026!@localhost:5432/financial_health_db
   ```

3. **Restart backend**:
   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn app.main:app --reload
   ```

4. **Check in pgAdmin**:
   - Refresh tables
   - You'll see your application tables created!

---

## pgAdmin Tips & Tricks

### Quick Tips:
- **F5**: Refresh
- **F7**: Open Query Tool
- **Ctrl+Enter**: Execute query
- **Ctrl+S**: Save query

### View Table Structure:
1. Right-click table → "Properties"
2. See columns, indexes, constraints

### Create Users Visually:
1. Expand "Login/Group Roles"
2. Right-click → "Create" → "Login/Group Role"
3. Fill in details
4. Save!

---

## Security Best Practices

✅ **Change default passwords**  
✅ **Use pgAdmin master password**  
✅ **Enable SSL connections** in production  
✅ **Regular backups** via pgAdmin  
✅ **Monitor connections** in Dashboard  

---

## Summary

**pgAdmin 4** is installing and will provide:
- 🖥️ Visual database management
- 📊 Easy data browsing
- 🔍 Query tool with syntax highlighting
- 📈 Performance monitoring
- 💾 Backup/restore tools
- 📤 Data import/export

**Once installed**:
1. Open pgAdmin 4
2. Add server connection (see Step 3 above)
3. View your application's data visually!
4. No more command line needed!

---

## Need Help?

All setup steps are in **POSTGRESQL_SETUP.md** for command-line setup.  
This guide covers pgAdmin 4 GUI setup!
