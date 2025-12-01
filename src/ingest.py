from pathlib import Path
from typing import List, Dict
import time

class DocumentIngestor:
    """Complete document ingestion pipeline"""
    
    def __init__(self, encryption_manager, embedding_generator, db_client):
        self.enc = encryption_manager
        self.emb = embedding_generator
        self.db = db_client
        self.stats = {
            'documents_processed': 0,
            'chunks_created': 0,
            'total_time': 0
        }
        print("✓ Document Ingestor initialized")
    
    def parse_document(self, file_path: str) -> Dict:
        """Parse document and extract text"""
        file_path = Path(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {
            'id': file_path.stem,
            'content': content,
            'file_path': str(file_path)
        }
    
    def chunk_text(self, text: str, chunk_size: int = 500):
        """Split text into chunks"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks if chunks else [text]
    
    def ingest_document(self, file_path: str):
        """Process and ingest single document"""
        start_time = time.time()
        
        print(f"\n[Processing] {Path(file_path).name}")
        
        # Parse
        doc = self.parse_document(file_path)
        print(f"  ✓ Parsed document ({len(doc['content'])} chars)")
        
        # Chunk
        chunks = self.chunk_text(doc['content'])
        print(f"  ✓ Created {len(chunks)} chunks")
        
        # Generate embeddings
        print(f"  → Generating embeddings...")
        embeddings = self.emb.generate_batch_embeddings(chunks)
        print(f"  ✓ Generated {len(embeddings)} embeddings")
        
        # Encrypt and prepare
        print(f"  → Encrypting and storing...")
        batch_docs = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = f"{doc['id']}_chunk_{idx}"
            encrypted_emb = self.enc.encrypt_vector(embedding)
            
            metadata = {
                'doc_id': doc['id'],
                'chunk_index': idx,
                'total_chunks': len(chunks),
                'content': chunk
            }
            
            batch_docs.append({
                'id': chunk_id,
                'vector': encrypted_emb,
                'metadata': metadata
            })
        
        # Store
        self.db.batch_insert(batch_docs)
        
        elapsed = time.time() - start_time
        self.stats['documents_processed'] += 1
        self.stats['chunks_created'] += len(chunks)
        self.stats['total_time'] += elapsed
        
        print(f"  ✓ Stored {len(batch_docs)} encrypted chunks ({elapsed:.2f}s)")
    
    def ingest_directory(self, directory: str, pattern: str = '*.txt'):
        """Ingest all documents in directory"""
        files = list(Path(directory).glob(pattern))
        
        print("="*70)
        print(f"Found {len(files)} files to process in {directory}")
        print("="*70)
        
        if len(files) == 0:
            print(f"\n⚠️  No {pattern} files found in {directory}")
            print(f"Make sure you have .txt files in that directory!")
            return
        
        for i, file_path in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}]", end=' ')
            try:
                self.ingest_document(str(file_path))
            except Exception as e:
                print(f"✗ Error: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n{'='*70}")
        print(f"INGESTION COMPLETE")
        print(f"{'='*70}")
        print(f"Documents processed: {self.stats['documents_processed']}")
        print(f"Chunks created: {self.stats['chunks_created']}")
        print(f"Total time: {self.stats['total_time']:.2f}s")
        print(f"{'='*70}")
