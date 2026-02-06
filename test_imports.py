#!/usr/bin/env python3
"""Test if all imports work correctly"""
import sys
sys.path.insert(0, 'backend')

print("Testing imports...")
print("-" * 60)

try:
    print("✓ Importing scipy...")
    from scipy import stats
    
    print("✓ Importing pandas...")
    import pandas as pd
    
    print("✓ Importing PyPDF2...")
    import PyPDF2
    
    print("✓ Importing file_parser...")
    from app.services.file_parser import file_parser
    
    print("✓ Importing financial_analysis...")
    from app.services.financial_analysis import financial_service
    
    print("✓ Importing ai_analysis...")
    from app.services.ai_analysis import ai_service
    
    print("-" * 60)
    print("✅ ALL IMPORTS SUCCESSFUL!")
    print("\nThe backend should now start without errors.")
    
except Exception as e:
    print(f"\n❌ Import failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
