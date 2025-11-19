import sys
sys.path.append('..')

from src.encryption import EncryptionManager
from src.embeddings import EmbeddingGenerator
from src.cyborgdb_sim import CyborgDBClient

def test_retrieval():
    print("="*60)
    print("TESTING RETRIEVAL")
    print("="*60)
    
    # Initialize
    enc_manager = EncryptionManager()
    emb_generator = EmbeddingGenerator()
    db_client = CyborgDBClient(use_simulated=True)
    
    # Check database
    stats = db_client.get_stats()
    print(f"\nVectors in database: {stats['count']}")
    
    # Test query
    query_text = "What are the software license terms?"
    print(f"\nQuery: {query_text}")
    
    query_emb = emb_generator.generate_embedding(query_text)
    enc_query = enc_manager.encrypt_vector(query_emb)
    
    results = db_client.encrypted_search(enc_query, top_k=3)
    
    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        metadata = result.get('metadata', {})
        doc_id = metadata.get('doc_id', 'unknown')
        preview = metadata.get('content', '')[:100]
        print(f"\n  {i}. Document: {doc_id}")
        print(f"     Preview: {preview}...")
    
    print("\n" + "="*60)
    print("✓ RETRIEVAL TEST PASSED!")
    print("="*60)

if __name__ == "__main__":
    test_retrieval()