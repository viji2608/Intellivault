import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import pickle

class SimulatedCyborgDB:
    """
    Simulated CyborgDB for development and testing.
    Mimics the real CyborgDB API but stores data locally.
    """
    
    def __init__(self, storage_path='data/cyborgdb_storage'):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.collections = {}
        self._load_collections()
        print(f"✓ Simulated CyborgDB initialized")
        print(f"  Storage: {self.storage_path.absolute()}")
    
    def _load_collections(self):
        """Load existing collections from disk"""
        manifest_file = self.storage_path / 'manifest.json'
        if manifest_file.exists():
            try:
                with open(manifest_file, 'r') as f:
                    self.collections = json.load(f)
                print(f"  ✓ Loaded {len(self.collections)} collections from manifest")
            except Exception as e:
                print(f"  ⚠ Could not load manifest: {e}")
        
        # Also check for .pkl files without manifest
        pkl_files = list(self.storage_path.glob('*.pkl'))
        for pkl_file in pkl_files:
            collection_name = pkl_file.stem
            if collection_name not in self.collections:
                # Reconstruct collection metadata from file
                try:
                    with open(pkl_file, 'rb') as f:
                        data = pickle.load(f)
                    self.collections[collection_name] = {
                        'count': len(data),
                        'dimension': 384  # Default
                    }
                    print(f"  ✓ Recovered collection '{collection_name}' with {len(data)} vectors")
                except Exception as e:
                    print(f"  ⚠ Could not load {pkl_file.name}: {e}")
    
    def _save_manifest(self):
        """Save collection metadata"""
        manifest_file = self.storage_path / 'manifest.json'
        with open(manifest_file, 'w') as f:
            json.dump(self.collections, f, indent=2)
    
    def create_collection(self, name: str, dimension: int, **kwargs):
        """Create a new collection for encrypted vectors"""
        if name in self.collections:
            print(f"  ℹ Collection '{name}' already exists")
            return
        
        self.collections[name] = {
            'dimension': dimension,
            'count': 0
        }
        
        # Create storage file
        collection_file = self.storage_path / f"{name}.pkl"
        if not collection_file.exists():
            with open(collection_file, 'wb') as f:
                pickle.dump([], f)
        
        self._save_manifest()
        print(f"✓ Created collection: {name} (dimension: {dimension})")
    
    def insert(self, collection: str, id: str, vector: Dict[str, Any], 
               metadata: Dict[str, Any]):
        """Insert encrypted vector with metadata"""
        collection_file = self.storage_path / f"{collection}.pkl"
        
        # Load existing data
        with open(collection_file, 'rb') as f:
            data = pickle.load(f)
        
        # Add new entry
        entry = {
            'id': id,
            'vector': vector,
            'metadata': metadata
        }
        data.append(entry)
        
        # Save
        with open(collection_file, 'wb') as f:
            pickle.dump(data, f)
        
        # Update count
        if collection in self.collections:
            self.collections[collection]['count'] += 1
            self._save_manifest()
    
    def batch_insert(self, collection: str, documents: List[Dict]):
        """Batch insert for efficiency"""
        collection_file = self.storage_path / f"{collection}.pkl"
        
        # Load existing
        if collection_file.exists():
            with open(collection_file, 'rb') as f:
                data = pickle.load(f)
        else:
            data = []
        
        # Add all
        data.extend(documents)
        
        # Save
        with open(collection_file, 'wb') as f:
            pickle.dump(data, f)
        
        # Update count
        if collection in self.collections:
            self.collections[collection]['count'] += len(documents)
        else:
            self.collections[collection] = {
                'count': len(documents),
                'dimension': 384
            }
        
        self._save_manifest()
        print(f"✓ Inserted {len(documents)} documents into '{collection}'")
    
    def search(self, collection: str, query_vector: Dict, 
               top_k: int = 5, **kwargs) -> List[Dict]:
        """
        Encrypted similarity search.
        """
        collection_file = self.storage_path / f"{collection}.pkl"
        
        if not collection_file.exists():
            return []
        
        with open(collection_file, 'rb') as f:
            data = pickle.load(f)
        
        if not data:
            return []
        
        # For simulation, return top_k results
        results = data[:min(top_k, len(data))]
        
        return results
    
    def get(self, collection: str, id: str) -> Dict:
        """Get document by ID"""
        collection_file = self.storage_path / f"{collection}.pkl"
        
        if not collection_file.exists():
            return None
        
        with open(collection_file, 'rb') as f:
            data = pickle.load(f)
        
        for entry in data:
            if entry['id'] == id:
                return entry
        
        return None
    
    def get_collection_stats(self, collection: str) -> Dict:
        """Get collection statistics"""
        if collection not in self.collections:
            return None
        
        return {
            'name': collection,
            'count': self.collections[collection]['count'],
            'dimension': self.collections[collection]['dimension']
        }


class CyborgDBClient:
    """
    Unified client that works with both simulated and real CyborgDB.
    """
    
    def __init__(self, use_simulated=True, host='localhost', port=8001):
        if use_simulated:
            self.client = SimulatedCyborgDB()
            self.mode = "SIMULATED"
        else:
            # Real CyborgDB connection
            try:
                import cyborgdb
                self.client = cyborgdb.Client(host=host, port=port)
                self.mode = "REAL"
            except ImportError:
                print("⚠️  CyborgDB not installed, using simulated mode")
                self.client = SimulatedCyborgDB()
                self.mode = "SIMULATED (fallback)"
        
        self.collection_name = "intellivault_vectors"
        print(f"✓ CyborgDB Client ready ({self.mode})")
    
    def create_collection(self, dimension: int):
        """Create collection"""
        self.client.create_collection(
            name=self.collection_name,
            dimension=dimension
        )
    
    def insert_encrypted_vector(self, doc_id: str, 
                                encrypted_vector: Dict,
                                metadata: Dict):
        """Insert single vector"""
        self.client.insert(
            collection=self.collection_name,
            id=doc_id,
            vector=encrypted_vector,
            metadata=metadata
        )
    
    def batch_insert(self, documents: List[Dict]):
        """Batch insert"""
        formatted_docs = []
        for doc in documents:
            formatted_docs.append({
                'id': doc['id'],
                'vector': doc['vector'],
                'metadata': doc['metadata']
            })
        
        self.client.batch_insert(
            collection=self.collection_name,
            documents=formatted_docs
        )
    
    def encrypted_search(self, query_vector: Dict, 
                        top_k: int = 5) -> List[Dict]:
        """Search"""
        return self.client.search(
            collection=self.collection_name,
            query_vector=query_vector,
            top_k=top_k
        )
    
    def get_by_id(self, doc_id: str) -> Dict:
        """Get by ID"""
        return self.client.get(
            collection=self.collection_name,
            id=doc_id
        )
    
    def get_stats(self) -> Dict:
        """Get stats"""
        return self.client.get_collection_stats(self.collection_name)
