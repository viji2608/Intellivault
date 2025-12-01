import random
from pathlib import Path

categories = ['legal', 'hr', 'finance', 'technical', 'compliance']
templates = {
    'legal': "CONFIDENTIAL LEGAL DOCUMENT\nMatter: {topic}\nPriority: {priority}\nDetails: {details}",
    'hr': "HUMAN RESOURCES - {topic}\nDate: 2024-Q{quarter}\nPolicy: {details}",
    'finance': "FINANCIAL REPORT - {topic}\nRevenue: ${amount}K\nGrowth: {growth}%\n{details}",
    'technical': "TECHNICAL SPECIFICATION\nSystem: {topic}\nVersion: {version}\n{details}",
    'compliance': "COMPLIANCE REQUIREMENT\nRegulation: {topic}\nStatus: {status}\n{details}"
}

topics = ['Licensing', 'Contracts', 'Benefits', 'Security', 'Performance', 'Strategy']
details_pool = [
    "Critical business information requiring strict confidentiality.",
    "Contains proprietary methodologies and trade secrets.",
    "Material non-public information for internal use only.",
    "Sensitive data requiring encryption and access controls."
]

Path('data/raw').mkdir(parents=True, exist_ok=True)

for i in range(50):
    cat = random.choice(categories)
    template = templates[cat]
    
    content = template.format(
        topic=random.choice(topics),
        priority=random.choice(['High', 'Medium', 'Critical']),
        quarter=random.randint(1,4),
        amount=random.randint(100,999),
        growth=random.randint(5,50),
        version=f"{random.randint(1,5)}.{random.randint(0,9)}",
        status=random.choice(['Active', 'In Review', 'Approved']),
        details=random.choice(details_pool)
    )
    
    filename = f"{cat}_{i:03d}.txt"
    with open(f'data/raw/{filename}', 'w') as f:
        f.write(content)

print(f"✓ Generated 50 additional documents")
