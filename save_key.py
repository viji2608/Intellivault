from src.encryption import EncryptionManager
import json
from pathlib import Path

def save_key():
    """Generate and save an encryption key"""
    
    # Create encryption manager
    em = EncryptionManager()
    
    # Get key as base64
    key_b64 = em.get_key_base64()
    
    # Save to secure location
    key_data = {
        'key': key_b64,
        'algorithm': 'AES-256-GCM',
        'note': 'IntelliVault master encryption key - KEEP SECURE!'
    }
    
    # Create config directory if it doesn't exist
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    
    # Save key
    key_file = config_dir / 'encryption_key.json'
    with open(key_file, 'w') as f:
        json.dump(key_data, f, indent=2)
    
    print(f"✓ Encryption key saved to: {key_file}")
    print("\n⚠️  IMPORTANT:")
    print("   1. Add 'config/encryption_key.json' to .gitignore")
    print("   2. Back up this file securely")
    print("   3. Never commit it to version control")
    print("   4. In production, use AWS KMS, Azure Key Vault, or similar")
    
    return key_file

def load_key():
    """Load existing encryption key"""
    
    key_file = Path('config/encryption_key.json')
    
    if not key_file.exists():
        print("✗ No key file found. Run save_key() first!")
        return None
    
    with open(key_file, 'r') as f:
        key_data = json.load(f)
    
    # Create encryption manager from saved key
    em = EncryptionManager.from_base64_key(key_data['key'])
    
    print(f"✓ Loaded encryption key from: {key_file}")
    return em

if __name__ == "__main__":
    print("Generating and saving encryption key...\n")
    save_key()