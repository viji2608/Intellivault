#!/usr/bin/env python3
"""
Complete ingestion script for IntelliVault.
Processes all documents in data/raw/ directory.
"""

from src.encryption import EncryptionManager
from src.embeddings import EmbeddingGenerator
from src.cyborgdb_sim import CyborgDBClient
from src.ingest import DocumentIngestor
import time

def main():
    print("\n" + "="*70)
    print("INTELLIVAULT - DOCUMENT INGESTION")
    print("="*70)
    
    start_time = time.time()
    
    # Initialize components
    print("\nInitializing components...")
    enc_manager = EncryptionManager()
    emb_generator = EmbeddingGenerator()
    db_client = CyborgDBClient(use_simulated=True)
    
    # Create collection
    db_client.create_collection(dimension=emb_generator.get_dimension())
    
    # Create ingestor
    ingestor = DocumentIngestor(enc_manager, emb_generator, db_client)
    
    print("\n✓ All components ready!")
    input("\nPress ENTER to start ingestion...")
    
    # *** THIS IS THE CRITICAL LINE - IT ACTUALLY INGESTS ***
    print("\nStarting document ingestion...\n")
    ingestor.ingest_directory('data/raw', pattern='*.txt')
    
    # Show final stats
    total_time = time.time() - start_time
    
    print(f"\n{'='*70}")
    print("FINAL STATISTICS")
    print(f"{'='*70}")
    
    stats = db_client.get_stats()
    if stats:
        print(f"Total vectors in database: {stats['count']}")
        print(f"Vector dimension: {stats['dimension']}")
    else:
        print("⚠️  No stats available")
    
    print(f"Total pipeline time: {total_time:.2f}s")
    print(f"{'='*70}")
    
    if stats and stats.get('count', 0) > 0:
        print("\n🎉 Phase 2 Complete!")
        print("\nYour encrypted knowledge base is ready!")
        print("\nNext step: Run 'cd tests && python test_retrieval.py'")
    else:
        print("\n⚠️  WARNING: No documents were processed!")
        print("Check that .txt files exist in data/raw/")

if __name__ == "__main__":
    main()
