import os
from pathlib import Path

DOCUMENTS = {
    'contract_software_license.txt': """
CONFIDENTIAL SOFTWARE LICENSE AGREEMENT
This Agreement is entered into between Acme Corporation.
LICENSE GRANT: Non-exclusive license for internal use.
PAYMENT TERMS: Annual fee $250,000 USD.
TERM: 3 years with automatic renewal.
""",
    
    'hr_remote_work_policy.txt': """
HUMAN RESOURCES POLICY - REMOTE WORK
Effective Date: March 1, 2024
SECURITY REQUIREMENTS: VPN, encryption, secure WiFi.
WORK HOURS: Core hours 10 AM - 3 PM local time.
EQUIPMENT: Company provides laptop, monitor.
""",
    
    'financial_q4_report.txt': """
CONFIDENTIAL FINANCIAL REPORT - Q4 2024
Total revenue: $5.2M (15% YoY growth)
Net profit: $1.1M (21% margin)
PROJECTIONS 2025: $7.5M - $8.2M expected revenue.
"""
}
def create_test_documents():
    data_dir = Path('data/raw')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("Creating test documents...")
    print("="*60)
    
    for filename, content in DOCUMENTS.items():
        filepath = data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        
        word_count = len(content.split())
        print(f"✓ Created: {filename} ({word_count} words)")
    
    print("="*60)
    print(f"✓ Created {len(DOCUMENTS)} test documents")
    print(f"✓ Location: {data_dir.absolute()}")

if __name__ == "__main__":
    create_test_documents()