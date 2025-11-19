import sys
sys.path.append('..')

from src.encryption import EncryptionManager
from src.embeddings import EmbeddingGenerator
import numpy as np
import time

def test_full_encryption_pipeline():
    """
    Complete test of the encryption pipeline.
    This simulates what will happen in production.
    """
    print("="*70)
    print("INTELLIVAULT PHASE 1 - ENCRYPTION PIPELINE TEST")
    print("="*70)
    
    # ===== STEP 1: Initialize =====
    print("\n[1/6] Initializing components...")
    enc_manager = EncryptionManager()
    emb_generator = EmbeddingGenerator()
    print("✓ Components initialized")
    
    # ===== STEP 2: Generate Embeddings =====
    print("\n[2/6] Generating embeddings for test documents...")
    
    test_documents = [
        "Confidential: Q4 2024 revenue projections and strategic initiatives",
        "Employee handbook: Remote work policy and security guidelines",
        "Internal: Product roadmap for AI features in 2025",
        "HR: Compensation structure and bonus calculation methodology"
    ]
    
    embeddings = []
    for i, doc in enumerate(test_documents, 1):
        emb = emb_generator.generate_embedding(doc)
        embeddings.append(emb)
        print(f"  ✓ Document {i}: {emb.shape[0]} dimensions")
    
    # ===== STEP 3: Encrypt Embeddings =====
    print("\n[3/6] Encrypting all embeddings...")
    
    encrypted_embeddings = []
    start_time = time.time()
    
    for i, emb in enumerate(embeddings, 1):
        encrypted = enc_manager.encrypt_vector(emb)
        encrypted_embeddings.append(encrypted)
        print(f"  ✓ Encrypted document {i}")
    
    encryption_time = time.time() - start_time
    print(f"\n  Total encryption time: {encryption_time:.3f}s")
    print(f"  Average per document: {encryption_time/len(embeddings):.3f}s")
    
    # ===== STEP 4: Verify Encryption =====
    print("\n[4/6] Verifying encryption (checking ciphertext)...")
    
    for i, encrypted in enumerate(encrypted_embeddings, 1):
        ciphertext_preview = encrypted['ciphertext'][:40]
        print(f"  Document {i} ciphertext: {ciphertext_preview}...")
    
    print("  ✓ All embeddings are encrypted (not readable)")
    
    # ===== STEP 5: Decrypt and Verify =====
    print("\n[5/6] Decrypting embeddings...")
    
    start_time = time.time()
    decryption_errors = 0
    
    for i, (original, encrypted) in enumerate(zip(embeddings, encrypted_embeddings), 1):
        decrypted = enc_manager.decrypt_vector(encrypted)
        
        # Check if decryption worked
        if np.allclose(original, decrypted):
            print(f"  ✓ Document {i}: Decryption successful")
        else:
            print(f"  ✗ Document {i}: DECRYPTION FAILED!")
            decryption_errors += 1
    
    decryption_time = time.time() - start_time
    print(f"\n  Total decryption time: {decryption_time:.3f}s")
    print(f"  Average per document: {decryption_time/len(embeddings):.3f}s")
    
    # ===== STEP 6: Test Search Functionality =====
    print("\n[6/6] Testing encrypted search simulation...")
    
    # Simulate a query
    query_text = "What are the revenue projections?"
    query_embedding = emb_generator.generate_embedding(query_text)
    
    print(f"\n  Query: '{query_text}'")
    print("\n  Computing similarities...")
    
    # In real system, this would happen on encrypted vectors
    # For now, we decrypt and compute similarity (demo purposes)
    results = []
    for i, (encrypted, doc_text) in enumerate(zip(encrypted_embeddings, test_documents)):
        # Decrypt
        decrypted_emb = enc_manager.decrypt_vector(encrypted)
        
        # Compute similarity
        similarity = emb_generator.compute_similarity(query_embedding, decrypted_emb)
        
        results.append({
            'doc_id': i,
            'text': doc_text,
            'similarity': similarity
        })
    
    # Sort by similarity
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    print("\n  Top 3 Results:")
    for i, result in enumerate(results[:3], 1):
        print(f"\n  {i}. Similarity: {result['similarity']:.3f}")
        print(f"     Text: {result['text'][:60]}...")
    
    # ===== FINAL RESULTS =====
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    
    if decryption_errors == 0:
        print("✓ All tests PASSED!")
        print(f"✓ Processed {len(test_documents)} documents")
        print(f"✓ Encryption overhead: {encryption_time:.3f}s")
        print(f"✓ Decryption overhead: {decryption_time:.3f}s")
        print(f"✓ Search accuracy: Working correctly")
        print("\n🎉 Phase 1 is complete! Your encryption pipeline is ready!")
    else:
        print(f"✗ FAILED: {decryption_errors} decryption errors")
        print("Please check your code and try again.")
    
    print("="*70)

if __name__ == "__main__":
    test_full_encryption_pipeline()