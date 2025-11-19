import json
import pickle
from pathlib import Path
from typing import List, Dict, Any

class SimulatedCyborgDB:
    """Simulated CyborgDB for development"""
    
    def __init__(self, storage_path='data/cyborgdb_storage'):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.collections = {}
        print(f"✓ Simulated CyborgDB initialized")
    
    def create_collection(self, name: str, dimension: int, **kwargs):
        """Create a new collection"""
        if name in self.collections:
            print(f"Collection '{name}' already exists")
            return
        
        self.collections[name] = {
            'dimension': dimension,
            'count': 0
        }
        
        collection_file = self.storage_path / f"{name}.pkl"
        
        # Initialize empty list in the file
        with open(collection_file, 'wb') as f:
            pickle.dump([], f)
        
        print(f"✓ Created collection: {name}")

    def batch_insert(self, collection: str, documents: List[Dict]):
        """Batch insert documents"""
        if collection not in self.collections:
            print(f"Error: Collection '{collection}' does not exist.")
            return

        collection_file = self.storage_path / f"{collection}.pkl"
        
        try:
            # Load existing data
            with open(collection_file, 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            data = []
        
        # Add new documents
        data.extend(documents)
        
        # Save back to file
        with open(collection_file, 'wb') as f:
            pickle.dump(data, f)
        
        self.collections[collection]['count'] += len(documents)
        print(f"✓ Inserted {len(documents)} documents into '{collection}'")
    
    def search(self, collection: str, query_vector: Dict, top_k: int = 5) -> List[Dict]:
        """
        Simulate search. 
        NOTE: In a real DB, this would calculate Cosine Similarity.
        Here, it returns the most recently added items (or just the first N).
        """
        collection_file = self.storage_path / f"{collection}.pkl"
        
        try:
            with open(collection_file, 'rb') as f:
                data = pickle.load(f)
            
            # Return top_k results (simulated)
            return data[:min(top_k, len(data))]
            
        except FileNotFoundError:
            print(f"Error: Collection '{collection}' not found.")
            return []

class CyborgDBClient:
    """Unified client"""
    
    def __init__(self, use_simulated=True):
        if use_simulated:
            self.client = SimulatedCyborgDB()
        self.collection_name = "intellivault_vectors"
        print("✓ CyborgDB Client ready")
    
    def create_collection(self, dimension: int):
        self.client.create_collection(
            name=self.collection_name,
            dimension=dimension
        )
    
    def batch_insert(self, documents: List[Dict]):
        self.client.batch_insert(
            collection=self.collection_name,
            documents=documents
        )
    
    def encrypted_search(self, query_vector: Dict, top_k: int = 5):
        return self.client.search(
            collection=self.collection_name,
            query_vector=query_vector,
            top_k=top_k
        )
    
    def get_stats(self):
        if self.collection_name in self.client.collections:
            return self.client.collections[self.collection_name]
        return None

# --- Optional: Usage Test Block ---
if __name__ == "__main__":
    # Initialize Client
    db = CyborgDBClient()
    
    # 1. Create Collection (e.g., 1536 dimensions for embeddings)
    db.create_collection(dimension=1536)
    
    # 2. Prepare Mock Data
    mock_docs = [
        {"id": "doc1", "vector": [0.1, 0.2], "content": "Hello World"},
        {"id": "doc2", "vector": [0.3, 0.4], "content": "Testing DB"}
    ]
    
    # 3. Insert Data
    db.batch_insert(mock_docs)
    
    # 4. Search Data
    results = db.encrypted_search(query_vector={"vector": [0.1, 0.2]})
    print(f"Search Results: {results}")