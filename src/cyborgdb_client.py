"""
Real CyborgDB integration using the official Docker service.
"""

import requests
import json
from typing import List, Dict, Any

class CyborgDBClient:
    """
    Client for real CyborgDB REST API.
    """
    
    def __init__(self, host='localhost', port=8001):
        self.base_url = f"http://{host}:{port}"
        self.collection_name = "intellivault_vectors"
        
        print(f"🔗 Connecting to CyborgDB at {self.base_url}")
        
        # Test connection
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✓ Connected to real CyborgDB!")
            else:
                print(f"⚠️  CyborgDB responded with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Could not connect to CyborgDB: {e}")
            print("  Make sure Docker container is running:")
            print("  docker run -d -p 8001:8001 cyborginc/cyborgdb-service")
            raise
    
    def create_collection(self, dimension: int):
        """Create encrypted vector collection"""
        payload = {
            "name": self.collection_name,
            "dimension": dimension,
            "encryption": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/collections",
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 201, 409]:  # 409 = already exists
                print(f"✓ Collection '{self.collection_name}' ready (dimension: {dimension})")
            else:
                print(f"⚠️  Collection creation returned {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error creating collection: {e}")
    
    def batch_insert(self, documents: List[Dict]):
        """Batch insert encrypted vectors"""
        payload = {
            "collection": self.collection_name,
            "documents": documents
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/insert",
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print(f"✓ Inserted {len(documents)} encrypted vectors")
            else:
                print(f"⚠️  Insert returned {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error inserting documents: {e}")
    
    def encrypted_search(self, query_vector: Dict, top_k: int = 5) -> List[Dict]:
        """Encrypted similarity search"""
        payload = {
            "collection": self.collection_name,
            "query_vector": query_vector,
            "top_k": top_k
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/search",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get("results", [])
            else:
                print(f"⚠️  Search returned {response.status_code}")
                print(f"Response: {response.text}")
                return []
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Get collection statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/collections/{self.collection_name}/stats",
                timeout=5
            )
            
            if response.status_code == 200:
                stats = response.json()
                return {
                    'name': self.collection_name,
                    'count': stats.get('count', 0),
                    'dimension': stats.get('dimension', 384)
                }
            else:
                return None
        except Exception as e:
            print(f"Error getting stats: {e}")
            return None


# Test script
if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING REAL CYBORGDB CONNECTION")
    print("="*70)
    
    try:
        client = CyborgDBClient()
        print("\n✓ Real CyborgDB integration successful!")
        print("\nNext steps:")
        print("1. Update ingest_all.py to use CyborgDBClient")
        print("2. Re-ingest your 143 documents")
        print("3. Test search with encrypted vectors")
    except Exception as e:
        print(f"\n✗ Integration failed: {e}")
        print("\nMake sure CyborgDB Docker container is running:")
        print("  docker run -d -p 8001:8001 cyborginc/cyborgdb-service")
    
    print("="*70 + "\n")
