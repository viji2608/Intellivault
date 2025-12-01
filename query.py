#!/usr/bin/env python3
from src.encryption import EncryptionManager
from src.embeddings import EmbeddingGenerator
from src.cyborgdb_sim import CyborgDBClient
from src.rag import RAGOrchestrator

def main():
    print("\n" + "="*70)
    print("INTELLIVAULT - KNOWLEDGE QUERY SYSTEM")
    print("="*70)
    print("Type your question or 'quit' to exit\n")
    
    # Initialize
    enc = EncryptionManager()
    emb = EmbeddingGenerator()
    db = CyborgDBClient(use_simulated=True)
    rag = RAGOrchestrator(enc, emb, db)
    
    print("\n✓ Ready!\n")
    
    # Query loop
    while True:
        query = input("💬 Question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break
        
        if not query:
            continue
        
        try:
            response = rag.query(query, top_k=3)
            
            print("\n" + "="*70)
            print("ANSWER:")
            print("="*70)
            print(response['answer'])
            print("\n" + "-"*70)
            print(f"Sources: {response['num_sources']}")
            for i, src in enumerate(response['sources'][:2], 1):
                doc = src['metadata'].get('doc_id', 'unknown')
                sim = src['similarity']
                print(f"  {i}. {doc} ({sim:.1%})")
            print("="*70 + "\n")
        
        except Exception as e:
            print(f"\n✗ Error: {e}\n")

if __name__ == "__main__":
    main()
