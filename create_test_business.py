#!/usr/bin/env python3
"""
Create a test business for upload testing
"""
import sys
import os

# Change to backend directory
os.chdir('backend')
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.business import Business, IndustryType, BusinessSize
from app.models.user import User
from app.core.security import get_password_hash

print("Creating test business...")
print("=" * 60)

db = SessionLocal()

try:
    # Check if business exists
    business = db.query(Business).filter(Business.id == 1).first()
    
    if not business:
        # Get or create user ID 1
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            print("Creating test user...")
            # Use pre-hashed password to avoid bcrypt issues
            user = User(
                id=1,
                email="test@example.com",
                username="testuser",
                full_name="Test User",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5uyilHHPVGFne",  # "password"
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✓ Created user: {user.email} (ID: {user.id})")
        else:
            print(f"✓ User exists: {user.email} (ID: {user.id})")
        
        print("\nCreating test business...")
        business = Business(
            user_id=1,
            business_name="Test Manufacturing Co.",
            legal_name="Test Manufacturing Company Pvt Ltd",
            registration_number="TEST123456",
            gst_number="29ABCDE1234F1Z5",
            pan_number="ABCDE1234F",
            industry=IndustryType.MANUFACTURING,
            business_size=BusinessSize.SMALL,
            address="123 Test Street",
            city="Mumbai",
            state="Maharashtra",
            pincode="400001",
            phone="+91-22-12345678",
            email="info@testmfg.com",
            annual_revenue=2500000.00,
            employee_count=25,
            established_year=2020
        )
        db.add(business)
        db.commit()
        db.refresh(business)
        print(f"✓ Created business: {business.business_name} (ID: {business.id})")
    else:
        print(f"\n✓ Business exists: {business.business_name} (ID: {business.id})")
    
    print("\n" + "=" * 60)
    print("✅ TEST DATA READY!")
    print(f"\nYou can now upload files using:")
    print(f"  business_id: {business.id}")
    print(f"  User: {user.email}")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
