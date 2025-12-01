from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import numpy as np
from pathlib import Path
import json

class EncryptionManager:
    """
    Handles encryption and decryption of embedding vectors.
    Uses AES-256-GCM for authenticated encryption.
    Automatically saves and loads encryption keys.
    """
    
    def __init__(self, master_key=None):
        """
        Initialize with a master encryption key.
        If no key provided, tries to load from config/encryption_key.json
        If no saved key exists, generates a new random 256-bit key.
        
        Args:
            master_key: Optional 32-byte key. If None, loads or generates key.
        """
        if master_key is not None:
            # User provided a key directly
            self.master_key = master_key
            print("✓ Using provided encryption key")
            return
        
        # Determine project root
        current_path = Path.cwd()
        if current_path.name == 'src' or current_path.name == 'tests':
            project_root = current_path.parent
        else:
            project_root = current_path
        
        key_file = project_root / 'config' / 'encryption_key.json'
        
        # Try to load existing key
        if key_file.exists():
            try:
                with open(key_file, 'r') as f:
                    key_data = json.load(f)
                self.master_key = base64.b64decode(key_data['key'])
                print("✓ Loaded existing encryption key")
                return
            except Exception as e:
                print(f"⚠️  Error loading key file: {e}")
                print("⚠️  Generating new key...")
        
        # No existing key found - generate new one
        self.master_key = get_random_bytes(32)
        print("⚠️  New encryption key generated!")
        
        # Save the new key
        self._save_key(project_root)
    
    def _save_key(self, project_root):
        """Save the encryption key to config directory"""
        try:
            config_dir = project_root / 'config'
            config_dir.mkdir(parents=True, exist_ok=True)
            
            key_data = {
                'key': base64.b64encode(self.master_key).decode('utf-8'),
                'algorithm': 'AES-256-GCM',
                'note': 'IntelliVault master encryption key - KEEP SECURE!'
            }
            
            key_file = config_dir / 'encryption_key.json'
            with open(key_file, 'w') as f:
                json.dump(key_data, f, indent=2)
            
            print(f"✓ Key saved to: {key_file.absolute()}")
            print("⚠️  IMPORTANT: Add 'config/encryption_key.json' to .gitignore")
        except Exception as e:
            print(f"⚠️  Could not save key: {e}")
    
    def encrypt_vector(self, vector):
        """Encrypt a numpy embedding vector"""
        vector_bytes = vector.tobytes()
        cipher = AES.new(self.master_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(vector_bytes)
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'nonce': base64.b64encode(cipher.nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8'),
            'shape': vector.shape,
            'dtype': str(vector.dtype)
        }
    
    def decrypt_vector(self, encrypted_data):
        """Decrypt an encrypted vector back to numpy array"""
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        nonce = base64.b64decode(encrypted_data['nonce'])
        tag = base64.b64decode(encrypted_data['tag'])
        
        cipher = AES.new(self.master_key, AES.MODE_GCM, nonce=nonce)
        vector_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        
        vector = np.frombuffer(vector_bytes, dtype=encrypted_data['dtype'])
        return vector.reshape(encrypted_data['shape'])
    
    def get_key_base64(self):
        """Export key as base64 string for storage"""
        return base64.b64encode(self.master_key).decode('utf-8')
    
    @classmethod
    def from_base64_key(cls, key_b64):
        """Load EncryptionManager from a stored key"""
        key = base64.b64decode(key_b64)
        return cls(master_key=key)


if __name__ == "__main__":
    print("="*70)
    print("TESTING ENCRYPTION MANAGER")
    print("="*70)
    
    current_path = Path.cwd()
    if current_path.name == 'src' or current_path.name == 'tests':
        project_root = current_path.parent
    else:
        project_root = current_path
    
    print(f"\nCurrent directory: {current_path}")
    print(f"Project root: {project_root}")
    
    key_file = project_root / 'config' / 'encryption_key.json'
    print(f"Key file path: {key_file}")
    print(f"Key file exists: {key_file.exists()}\n")
    
    print("[Test 1] Creating EncryptionManager...")
    em1 = EncryptionManager()
    
    print("\n[Test 2] Testing encryption/decryption...")
    test_vector = np.array([1.5, 2.7, -0.3, 4.2])
    print(f"Original: {test_vector}")
    
    encrypted = em1.encrypt_vector(test_vector)
    print(f"Encrypted: {encrypted['ciphertext'][:30]}...")
    
    decrypted = em1.decrypt_vector(encrypted)
    print(f"Decrypted: {decrypted}")
    
    if np.allclose(test_vector, decrypted):
        print("✓ Encryption/Decryption works!")
    else:
        print("✗ FAILED!")
    
    print("\n[Test 3] Testing key persistence...")
    print("Creating second EncryptionManager...")
    em2 = EncryptionManager()
    
    if em1.get_key_base64() == em2.get_key_base64():
        print("✓ Same key loaded!")
    else:
        print("✗ Different keys!")
    
    print("\n[Test 4] Cross-instance decryption...")
    try:
        decrypted2 = em2.decrypt_vector(encrypted)
        if np.allclose(test_vector, decrypted2):
            print("✓ Second instance can decrypt first instance's data!")
        else:
            print("✗ Wrong result!")
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if key_file.exists():
        print(f"✓ Key file: {key_file}")
        with open(key_file, 'r') as f:
            key_data = json.load(f)
        print(f"✓ Key preview: {key_data['key'][:20]}...")
    
    print("\n✓ All tests completed!")
    print("="*70)
