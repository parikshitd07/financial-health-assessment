"""
File Parsing Service
Handles parsing of CSV, Excel, and PDF financial documents
"""
from typing import Dict, Any, Optional
import pandas as pd
import io
from datetime import datetime
import re


class FileParserService:
    """Service for parsing financial documents"""
    
    def parse_file(self, file_content: bytes, filename: str, file_type: str) -> Dict[str, Any]:
        """
        Parse uploaded file and extract financial data
        
        Args:
            file_content: File content as bytes
            filename: Name of the uploaded file
            file_type: MIME type or file extension
        
        Returns:
            Dictionary containing extracted financial data
        """
        # Determine file type
        if file_type in ['text/csv', 'application/vnd.ms-excel'] or filename.endswith('.csv'):
            return self._parse_csv(file_content, filename)
        elif file_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'] or filename.endswith(('.xlsx', '.xls')):
            return self._parse_excel(file_content, filename)
        elif file_type == 'application/pdf' or filename.endswith('.pdf'):
            # For PDFs, return raw bytes to be sent directly to Gemini
            return {
                'document_type': 'pdf',
                'raw_pdf_bytes': file_content,
                'filename': filename
            }
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _parse_csv(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Parse CSV file"""
        try:
            # Read CSV
            df = pd.read_csv(io.BytesIO(file_content))
            
            # Detect document type from filename or content
            doc_type = self._detect_document_type(filename, df)
            
            if doc_type == 'balance_sheet':
                return self._parse_balance_sheet(df)
            elif doc_type == 'profit_loss':
                return self._parse_profit_loss(df)
            elif doc_type == 'cash_flow':
                return self._parse_cash_flow(df)
            else:
                # Generic parsing
                return self._parse_generic(df)
                
        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {str(e)}")
    
    def _parse_excel(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Parse Excel file"""
        try:
            # Read Excel (first sheet)
            df = pd.read_excel(io.BytesIO(file_content), sheet_name=0)
            
            # Detect document type
            doc_type = self._detect_document_type(filename, df)
            
            if doc_type == 'balance_sheet':
                return self._parse_balance_sheet(df)
            elif doc_type == 'profit_loss':
                return self._parse_profit_loss(df)
            elif doc_type == 'cash_flow':
                return self._parse_cash_flow(df)
            else:
                return self._parse_generic(df)
                
        except Exception as e:
            raise ValueError(f"Failed to parse Excel: {str(e)}")
    
    def _parse_pdf(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Parse PDF file (simplified - would need OCR for scanned PDFs)"""
        try:
            import PyPDF2
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Extract financial data using regex patterns
            return self._extract_from_text(text)
            
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}. Note: Only text-based PDFs are supported.")
    
    def _detect_document_type(self, filename: str, df: pd.DataFrame) -> str:
        """Detect the type of financial document"""
        filename_lower = filename.lower()
        
        # Check filename
        if any(term in filename_lower for term in ['balance', 'sheet', 'position']):
            return 'balance_sheet'
        elif any(term in filename_lower for term in ['profit', 'loss', 'p&l', 'income', 'statement']):
            return 'profit_loss'
        elif any(term in filename_lower for term in ['cash', 'flow', 'cashflow']):
            return 'cash_flow'
        
        # Check column names
        columns_lower = ' '.join(df.columns.astype(str).str.lower())
        
        if any(term in columns_lower for term in ['asset', 'liability', 'equity']):
            return 'balance_sheet'
        elif any(term in columns_lower for term in ['revenue', 'expense', 'profit']):
            return 'profit_loss'
        elif any(term in columns_lower for term in ['operating', 'investing', 'financing']):
            return 'cash_flow'
        
        return 'unknown'
    
    def _parse_balance_sheet(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Parse balance sheet data"""
        data = {
            'document_type': 'balance_sheet',
            'total_assets': 0.0,
            'current_assets': 0.0,
            'cash_and_equivalents': 0.0,
            'accounts_receivable': 0.0,
            'inventory': 0.0,
            'fixed_assets': 0.0,
            'total_liabilities': 0.0,
            'current_liabilities': 0.0,
            'accounts_payable': 0.0,
            'short_term_debt': 0.0,
            'long_term_debt': 0.0,
            'owners_equity': 0.0
        }
        
        # Convert to lowercase for easier matching
        df.columns = df.columns.str.lower().str.strip()
        
        # Try to find the amount column
        amount_col = None
        for col in df.columns:
            if 'amount' in col or 'value' in col or 'balance' in col or col.replace(' ', '').replace('₹', '').replace(',', '').replace('.', '').isdigit():
                amount_col = col
                break
        
        if amount_col is None and len(df.columns) >= 2:
            amount_col = df.columns[-1]  # Use last column as amount
        
        # Parse each row
        for idx, row in df.iterrows():
            try:
                # Get item name (first column typically)
                item = str(row.iloc[0]).lower().strip() if len(row) > 0 else ""
                
                # Get amount
                amount = self._extract_number(row[amount_col]) if amount_col else 0.0
                
                # Map to fields
                if 'cash' in item or 'bank' in item:
                    data['cash_and_equivalents'] += amount
                elif 'receivable' in item or 'debtor' in item:
                    data['accounts_receivable'] += amount
                elif 'inventory' in item or 'stock' in item:
                    data['inventory'] += amount
                elif 'current asset' in item:
                    data['current_assets'] = amount
                elif 'fixed asset' in item or 'ppe' in item or 'property' in item:
                    data['fixed_assets'] += amount
                elif 'total asset' in item:
                    data['total_assets'] = amount
                elif 'payable' in item or 'creditor' in item:
                    data['accounts_payable'] += amount
                elif 'short' in item and 'debt' in item:
                    data['short_term_debt'] += amount
                elif 'long' in item and 'debt' in item:
                    data['long_term_debt'] += amount
                elif 'current liab' in item:
                    data['current_liabilities'] = amount
                elif 'total liab' in item:
                    data['total_liabilities'] = amount
                elif 'equity' in item or 'capital' in item:
                    data['owners_equity'] += amount
                    
            except Exception:
                continue
        
        # Calculate derived values if not provided
        if data['current_assets'] == 0:
            data['current_assets'] = (data['cash_and_equivalents'] + 
                                     data['accounts_receivable'] + 
                                     data['inventory'])
        
        if data['total_assets'] == 0:
            data['total_assets'] = data['current_assets'] + data['fixed_assets']
        
        if data['current_liabilities'] == 0:
            data['current_liabilities'] = (data['accounts_payable'] + 
                                          data['short_term_debt'])
        
        if data['total_liabilities'] == 0:
            data['total_liabilities'] = data['current_liabilities'] + data['long_term_debt']
        
        return data
    
    def _parse_profit_loss(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Parse profit & loss statement"""
        data = {
            'document_type': 'profit_loss',
            'total_revenue': 0.0,
            'cost_of_goods_sold': 0.0,
            'total_expenses': 0.0,
            'operating_expenses': 0.0,
            'salaries_wages': 0.0,
            'rent': 0.0,
            'utilities': 0.0,
            'marketing': 0.0,
            'other_expenses': 0.0
        }
        
        # Convert to lowercase
        df.columns = df.columns.str.lower().str.strip()
        
        # Find amount column
        amount_col = None
        for col in df.columns:
            if 'amount' in col or 'value' in col or col.replace(' ', '').replace('₹', '').replace(',', '').replace('.', '').isdigit():
                amount_col = col
                break
        
        if amount_col is None and len(df.columns) >= 2:
            amount_col = df.columns[-1]
        
        # Parse each row
        for idx, row in df.iterrows():
            try:
                item = str(row.iloc[0]).lower().strip() if len(row) > 0 else ""
                amount = self._extract_number(row[amount_col]) if amount_col else 0.0
                
                # Map to fields
                if 'revenue' in item or 'sales' in item or 'income' in item:
                    data['total_revenue'] += amount
                elif 'cogs' in item or 'cost of goods' in item or 'cost of sales' in item:
                    data['cost_of_goods_sold'] += amount
                elif 'salary' in item or 'wage' in item or 'payroll' in item:
                    data['salaries_wages'] += amount
                elif 'rent' in item or 'lease' in item:
                    data['rent'] += amount
                elif 'utility' in item or 'utilities' in item or 'electric' in item:
                    data['utilities'] += amount
                elif 'marketing' in item or 'advertising' in item:
                    data['marketing'] += amount
                elif 'operating expense' in item or 'opex' in item:
                    data['operating_expenses'] = amount
                elif 'expense' in item or 'cost' in item:
                    data['other_expenses'] += amount
                    
            except Exception:
                continue
        
        # Calculate derived values
        if data['operating_expenses'] == 0:
            data['operating_expenses'] = (data['salaries_wages'] + 
                                         data['rent'] + 
                                         data['utilities'] + 
                                         data['marketing'] + 
                                         data['other_expenses'])
        
        data['total_expenses'] = data['cost_of_goods_sold'] + data['operating_expenses']
        
        return data
    
    def _parse_cash_flow(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Parse cash flow statement"""
        data = {
            'document_type': 'cash_flow',
            'operating_cash_flow': 0.0,
            'investing_cash_flow': 0.0,
            'financing_cash_flow': 0.0
        }
        
        # Convert to lowercase
        df.columns = df.columns.str.lower().str.strip()
        
        # Find amount column
        amount_col = None
        for col in df.columns:
            if 'amount' in col or 'value' in col or 'cash' in col:
                amount_col = col
                break
        
        if amount_col is None and len(df.columns) >= 2:
            amount_col = df.columns[-1]
        
        # Parse each row
        for idx, row in df.iterrows():
            try:
                item = str(row.iloc[0]).lower().strip() if len(row) > 0 else ""
                amount = self._extract_number(row[amount_col]) if amount_col else 0.0
                
                if 'operating' in item:
                    data['operating_cash_flow'] = amount
                elif 'investing' in item:
                    data['investing_cash_flow'] = amount
                elif 'financing' in item:
                    data['financing_cash_flow'] = amount
                    
            except Exception:
                continue
        
        return data
    
    def _parse_generic(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generic parsing for unknown document types"""
        data = {
            'document_type': 'generic',
            'parsed_data': {}
        }
        
        # Try to extract key financial metrics
        df.columns = df.columns.str.lower().str.strip()
        
        for idx, row in df.iterrows():
            try:
                if len(row) >= 2:
                    key = str(row.iloc[0]).lower().strip()
                    value = self._extract_number(row.iloc[1])
                    
                    if value != 0:
                        data['parsed_data'][key] = value
            except Exception:
                continue
        
        return data
    
    def _extract_number(self, value) -> float:
        """Extract numeric value from string or number"""
        if pd.isna(value):
            return 0.0
        
        if isinstance(value, (int, float)):
            return float(value)
        
        # Convert to string and clean
        value_str = str(value).replace('₹', '').replace(',', '').replace('Rs', '').strip()
        
        # Handle negative values in parentheses
        if '(' in value_str and ')' in value_str:
            value_str = '-' + value_str.replace('(', '').replace(')', '')
        
        # Extract number using regex
        match = re.search(r'-?\d+\.?\d*', value_str)
        if match:
            return float(match.group())
        
        return 0.0
    
    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        """Extract financial data from text (for PDFs)"""
        data = {
            'document_type': 'text_extract',
            'extracted_values': {}
        }
        
        # Define patterns for common financial terms
        patterns = {
            'total_revenue': r'(?:total\s+)?revenue[:\s]+₹?[\s,]*(\d+(?:,\d+)*(?:\.\d+)?)',
            'total_assets': r'(?:total\s+)?assets[:\s]+₹?[\s,]*(\d+(?:,\d+)*(?:\.\d+)?)',
            'total_liabilities': r'(?:total\s+)?liabilities[:\s]+₹?[\s,]*(\d+(?:,\d+)*(?:\.\d+)?)',
            'cash': r'cash[:\s]+₹?[\s,]*(\d+(?:,\d+)*(?:\.\d+)?)',
        }
        
        text_lower = text.lower()
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text_lower)
            if match:
                value_str = match.group(1).replace(',', '')
                data['extracted_values'][key] = float(value_str)
        
        return data


# Create singleton instance
file_parser = FileParserService()
