#!/usr/bin/env python3
"""
Test retrieval from the encrypted vector database.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Change to project root so paths work correctly
import os
os.chdir(Path(__file__).parent.parent)

from src.encryption import EncryptionManager
from src.embeddings import EmbeddingGenerator
from src.cyborgdb_sim import CyborgDBClient

def test_retrieval():
    print("="*60)
    print("TESTING RETRIEVAL")
    print("="*60)
    print(f"Working directory: {Path.cwd()}")
    
    # Initialize
    print("\n[1/3] Initializing components...")
    enc_manager = EncryptionManager()
    emb_generator = EmbeddingGenerator()
    db_client = CyborgDBClient(use_simulated=True)
    
    # Check database
    print("\n[2/3] Checking database...")
    stats = db_client.get_stats()
    
    if stats is None:
        print("  ✗ No collection found!")
        print("  Run: python ingest_all.py")
        return
    
    if stats.get('count', 0) == 0:
        print("  ✗ Collection is empty!")
        print("  Run: python ingest_all.py")
        return
    
    print(f"  ✓ Vectors stored: {stats['count']}")
    print(f"  ✓ Dimension: {stats['dimension']}")
    
    # Test query
    print("\n[3/3] Testing search...")
    query_text = "What are the software license terms?"
    print(f"Query: '{query_text}'")
    
    query_emb = emb_generator.generate_embedding(query_text)
    enc_query = enc_manager.encrypt_vector(query_emb)
    results = db_client.encrypted_search(enc_query, top_k=3)
    
    if not results:
        print("  ⚠ No results found")
        return
    
    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        metadata = result.get('metadata', {})
        doc_id = metadata.get('doc_id', 'unknown')
        content = metadata.get('content', '')[:100]
        print(f"\n  {i}. Document: {doc_id}")
        print(f"     Preview: {content}...")
    
    print("\n" + "="*60)
    print("✓ RETRIEVAL TEST PASSED!")
    print("="*60)

if __name__ == "__main__":
    test_retrieval()
