from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import numpy as np

class EncryptionManager:
    """
    Handles encryption and decryption of embedding vectors.
    Uses AES-256-GCM for authenticated encryption.
    """
    
    def __init__(self, master_key=None):
        """
        Initialize with a master encryption key.
        If no key provided, generates a new random 256-bit key.
        
        Args:
            master_key: Optional 32-byte key. If None, generates new key.
        """
        if master_key is None:
            # Generate a secure random 256-bit (32-byte) key
            self.master_key = get_random_bytes(32)
            print("⚠️  New encryption key generated!")
            print("⚠️  Save this key securely - you'll need it to decrypt data!")
        else:
            self.master_key = master_key
            print("✓ Loaded existing encryption key")
    
    def encrypt_vector(self, vector):
        """
        Encrypt a numpy embedding vector.
        
        Args:
            vector: numpy array (the embedding)
            
        Returns:
            dict with encrypted data and metadata
        """
        # Step 1: Convert numpy array to bytes
        vector_bytes = vector.tobytes()
        
        # Step 2: Create cipher with random nonce (IV)
        cipher = AES.new(self.master_key, AES.MODE_GCM)
        
        # Step 3: Encrypt and get authentication tag
        ciphertext, tag = cipher.encrypt_and_digest(vector_bytes)
        
        # Step 4: Package everything for storage
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'nonce': base64.b64encode(cipher.nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8'),
            'shape': vector.shape,  # We need this to reconstruct
            'dtype': str(vector.dtype)  # And this too
        }
    
    def decrypt_vector(self, encrypted_data):
        """
        Decrypt an encrypted vector back to numpy array.
        
        Args:
            encrypted_data: dict from encrypt_vector()
            
        Returns:
            numpy array (original embedding)
        """
        # Step 1: Decode from base64
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        nonce = base64.b64decode(encrypted_data['nonce'])
        tag = base64.b64decode(encrypted_data['tag'])
        
        # Step 2: Create cipher with original nonce
        cipher = AES.new(self.master_key, AES.MODE_GCM, nonce=nonce)
        
        # Step 3: Decrypt and verify authentication tag
        vector_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        
        # Step 4: Reconstruct numpy array
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


# Quick test when running this file directly
if __name__ == "__main__":
    print("Testing EncryptionManager...")
    
    # Create manager
    em = EncryptionManager()
    
    # Create test vector
    test_vector = np.array([1.5, 2.7, -0.3, 4.2])
    print(f"Original: {test_vector}")
    
    # Encrypt
    encrypted = em.encrypt_vector(test_vector)
    print(f"Encrypted: {encrypted['ciphertext'][:30]}...")
    
    # Decrypt
    decrypted = em.decrypt_vector(encrypted)
    print(f"Decrypted: {decrypted}")
    
    # Verify they match
    if np.allclose(test_vector, decrypted):
        print("✓ Success! Encryption/Decryption working!")
    else:
        print("✗ Error! Vectors don't match!")