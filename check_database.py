from src.cyborgdb_sim import CyborgDBClient
from pathlib import Path

# Check database
db = CyborgDBClient(use_simulated=True)
stats = db.get_stats()

print("="*60)
print("DATABASE STATUS")
print("="*60)

if stats:
    print(f"Total vectors: {stats['count']}")
    print(f"Dimension: {stats['dimension']}")
    print(f"Collection: {stats['name']}")
else:
    print("No collection found!")

print("\n" + "="*60)
print("FILES IN data/raw/")
print("="*60)

files = list(Path('data/raw').glob('*.txt'))
print(f"Total files: {len(files)}")
print("\nFirst 10 files:")
for f in files[:10]:
    print(f"  - {f.name}")

print("\n" + "="*60)
print("STORAGE FILES")
print("="*60)

storage = Path('data/cyborgdb_storage')
for f in storage.glob('*'):
    size = f.stat().st_size / 1024
    print(f"  {f.name}: {size:.1f} KB")
