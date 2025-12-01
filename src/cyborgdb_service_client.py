"""
Real CyborgDB Service integration - CORRECTED.
"""

import os
from typing import List, Dict, Any, Optional
import numpy as np

# Try different import methods
try:
    from cyborgdb_core import CyborgDB
    CLIENT_TYPE = "core"
except:
    try:
        import cyborgdb_service
        CLIENT_TYPE = "service"
    except:
        raise ImportError("Could not import CyborgDB client")

class CyborgDBServiceClient:
    """
    Production CyborgDB Service client.
    """
    
    def __init__(self, api_key: str):
        """Initialize CyborgDB client."""
        self.api_key = api_key
        self.collection_name = "intellivault_vectors"
        
        print("🔗 Connecting to CyborgDB...")
        
        try:
            if CLIENT_TYPE == "core":
                # Using cyborgdb-core
                self.client = CyborgDB(api_key=api_key)
                print("✓ Using cyborgdb-core client")
            else:
                # Using cyborgdb-service
                self.client = cyborgdb_service.CyborgDB(api_key=api_key)
                print("✓ Using cyborgdb-service client")
            
            print("✓ Connected to CyborgDB!")
            
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            print("\nTrying alternative approach...")
            
            # Fallback: use the service directly
            try:
                from cyborgdb_core import create_client
                self.client = create_client(api_key=api_key)
                print("✓ Connected using create_client!")
            except:
                raise
    
    def create_collection(self, dimension: int):
        """Create encrypted vector collection"""
        try:
            # Create index (CyborgDB terminology)
            self.index = self.client.create_index(
                name=self.collection_name,
                dimension=dimension,
                metric="cosine"
            )
            print(f"✓ Index '{self.collection_name}' created (dimension: {dimension})")
        except Exception as e:
            # Index might already exist
            try:
                self.index = self.client.get_index(self.collection_name)
                print(f"✓ Using existing index '{self.collection_name}'")
            except:
                print(f"⚠️  Error: {e}")
    
    def batch_insert(self, documents: List[Dict]) -> bool:
        """Batch insert vectors"""
        try:
            # Prepare data
            ids = []
            vectors = []
            metadatas = []
            
            from src.encryption import EncryptionManager
            enc = EncryptionManager()
            
            for doc in documents:
                ids.append(doc['id'])
                # Decrypt vector (CyborgDB handles encryption)
                vector = enc.decrypt_vector(doc['vector'])
                vectors.append(vector.tolist())
                metadatas.append(doc['metadata'])
            
            # Insert
            self.index.upsert(
                ids=ids,
                vectors=vectors,
                metadata=metadatas
            )
            
            print(f"✓ Inserted {len(documents)} vectors into CyborgDB")
            return True
            
        except Exception as e:
            print(f"⚠️  Insert error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def encrypted_search(self, query_vector: Dict, top_k: int = 5) -> List[Dict]:
        """Search vectors"""
        try:
            from src.encryption import EncryptionManager
            enc = EncryptionManager()
            
            # Decrypt query
            query = enc.decrypt_vector(query_vector)
            
            # Search
            results = self.index.query(
                vector=query.tolist(),
                top_k=top_k
            )
            
            # Format results
            formatted = []
            for result in results:
                formatted.append({
                    'id': result['id'],
                    'vector': query_vector,
                    'metadata': result.get('metadata', {})
                })
            
            return formatted
            
        except Exception as e:
            print(f"⚠️  Search error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_stats(self) -> Optional[Dict]:
        """Get statistics"""
        try:
            stats = self.index.describe()
            return {
                'name': self.collection_name,
                'count': stats.get('vector_count', 0),
                'dimension': stats.get('dimension', 384)
            }
        except Exception as e:
            print(f"⚠️  Stats error: {e}")
            return None


if __name__ == "__main__":
    import sys
    
    api_key = os.getenv("CYBORGDB_API_KEY", "cyborg_ce554d85bbfc451aa4d332a94c94f1fe")
    
    print("="*70)
    print("TESTING CYBORGDB")
    print("="*70)
    
    try:
        client = CyborgDBServiceClient(api_key=api_key)
        print("\n✅ Connection successful!")
        print("\nYou can now run: python ingest_to_cyborgdb.py")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nDebugging info:")
        import cyborgdb_core
        print(f"Available in cyborgdb_core: {dir(cyborgdb_core)}")
