#!/usr/bin/env python3
"""
Test script for file upload and analysis functionality
"""
import sys
sys.path.insert(0, 'backend')

from app.services.file_parser import file_parser

# Test with sample balance sheet
print("Testing file parser with sample_balance_sheet.csv...")
print("="*60)

with open('sample_data/sample_balance_sheet.csv', 'rb') as f:
    content = f.read()
    
try:
    result = file_parser.parse_file(content, 'sample_balance_sheet.csv', 'text/csv')
    print("✅ File parsed successfully!")
    print(f"\nDocument Type: {result.get('document_type')}")
    print("\nParsed Financial Data:")
    print("-"*60)
    
    for key, value in result.items():
        if key != 'document_type' and isinstance(value, (int, float)):
            print(f"{key:30s}: ₹{value:,.2f}")
    
    print("\n" + "="*60)
    print("✅ TEST PASSED - File parsing is working!")
    
except Exception as e:
    print(f"❌ TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
