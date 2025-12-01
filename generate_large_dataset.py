import random
from pathlib import Path

categories = {
    'contracts': [
        'Software License Agreement', 'Service Level Agreement',
        'Non-Disclosure Agreement', 'Partnership Agreement',
        'Vendor Contract', 'Employment Agreement'
    ],
    'hr': [
        'Remote Work Policy', 'Code of Conduct', 'Benefits Package',
        'Performance Review Guidelines', 'Hiring Policy',
        'Termination Procedures'
    ],
    'finance': [
        'Q1 Financial Report', 'Q2 Financial Report',
        'Budget Allocation', 'Expense Policy', 'Revenue Forecast',
        'Investment Strategy'
    ],
    'legal': [
        'Compliance Requirements', 'Risk Assessment',
        'Litigation Summary', 'IP Portfolio', 'Regulatory Filing',
        'Audit Report'
    ],
    'technical': [
        'API Documentation', 'Security Architecture',
        'System Design', 'Infrastructure Plan', 'Disaster Recovery',
        'Technical Roadmap'
    ]
}

def generate_document(category, doc_type, idx):
    return f"""CONFIDENTIAL - {doc_type.upper()}
Document ID: {category.upper()}-{idx:03d}
Classification: Internal Use Only
Date: 2024-Q{random.randint(1,4)}

{doc_type} content for {category} department.
This is a sample confidential document containing sensitive business information.
Revenue data: ${random.randint(100,999)}K
Employee count: {random.randint(10,100)}
Strategic priority: {'High' if random.random() > 0.5 else 'Medium'}

Key details and information about {doc_type.lower()}.
Contains proprietary methodologies and confidential analysis.
Not for external distribution without proper authorization.
"""

# Generate 100 documents
data_dir = Path('data/raw')
data_dir.mkdir(parents=True, exist_ok=True)

count = 0
for category, doc_types in categories.items():
    for doc_type in doc_types:
        for i in range(3):  # 3 docs per type
            filename = f"{category}_{doc_type.replace(' ', '_').lower()}_{i+1}.txt"
            filepath = data_dir / filename
            
            content = generate_document(category, doc_type, count)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            count += 1
            if count >= 100:
                break
        if count >= 100:
            break
    if count >= 100:
        break

print(f"✓ Generated {count} confidential documents")
print(f"✓ Location: {data_dir.absolute()}")
