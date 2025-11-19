from src.encryption import EncryptionManager
from src.embeddings import EmbeddingGenerator
from src.cyborgdb_sim import CyborgDBClient
from src.ingest import DocumentIngestor

def main():
    print("\n" + "="*70)
    print("INTELLIVAULT - DOCUMENT INGESTION")
    print("="*70)
    
    # Initialize
    print("\nInitializing components...")
    enc_manager = EncryptionManager()
    emb_generator = EmbeddingGenerator()
    db_client = CyborgDBClient(use_simulated=True)
    
    # Create collection
    db_client.create_collection(
        dimension=emb_generator.get_dimension()
    )
    
    # Create ingestor
    ingestor = DocumentIngestor(
        enc_manager, emb_generator, db_client
    )
    
    print("\n✓ Ready to ingest!\n")
    input("Press ENTER to start...")
    
    # Ingest all
    ingestor.ingest_directory('data/raw', pattern='*.txt')
    
    print("\n🎉 Phase 2 Complete!")
    print("Your encrypted knowledge base is ready!")

if __name__ == "__main__":
    main()