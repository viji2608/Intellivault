#!/usr/bin/env python3
"""
Ingest all documents into REAL CyborgDB Service.
"""

import os
from pathlib import Path

# Set API key
os.environ["CYBORGDB_API_KEY"] = "cyborg_ce554d85bbfc451aa4d332a94c94f1fe"

from src.encryption import EncryptionManager
from src.embeddings import EmbeddingGenerator
from src.cyborgdb_service_client import CyborgDBServiceClient
from src.ingest import DocumentIngestor

def main():
    print("\n" + "="*70)
    print("INTELLIVAULT - REAL CYBORGDB INGESTION")
    print("="*70)
    
    # Initialize with REAL CyborgDB
    print("\n[1/4] Initializing components...")
    enc_manager = EncryptionManager()
    emb_generator = EmbeddingGenerator()
    db_client = CyborgDBServiceClient(
        api_key=os.getenv("CYBORGDB_API_KEY")
    )
    
    # Create collection
    print("\n[2/4] Creating collection...")
    db_client.create_collection(dimension=emb_generator.get_dimension())
    
    # Create ingestor
    ingestor = DocumentIngestor(enc_manager, emb_generator, db_client)
    
    print("\n[3/4] Ready to ingest to REAL CyborgDB!")
    input("\nPress ENTER to start ingestion...")
    
    # Ingest all documents
    print("\n[4/4] Starting ingestion...")
    ingestor.ingest_directory('data/raw', pattern='*.txt')
    
    # Show stats
    print("\n" + "="*70)
    print("INGESTION COMPLETE")
    print("="*70)
    
    stats = db_client.get_stats()
    if stats:
        print(f"✓ Total vectors in CyborgDB: {stats['count']}")
        print(f"✓ Vector dimension: {stats['dimension']}")
    
    print("\n🎉 Your documents are now in REAL CyborgDB!")
    print("="*70)

if __name__ == "__main__":
    main()
