from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingGenerator:
    """
    Generates embeddings (vector representations) from text.
    Uses pre-trained sentence transformer models.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the sentence-transformer model
                       'all-MiniLM-L6-v2' is fast and good quality (384 dims)
        """
        print(f"Loading embedding model: {model_name}")
        print("This may take a minute on first run...")
        
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        print(f"✓ Model loaded!")
        print(f"✓ Embedding dimension: {self.dimension}")
    
    def generate_embedding(self, text):
        """
        Generate embedding for a single piece of text.
        
        Args:
            text: String to embed
            
        Returns:
            numpy array (embedding vector)
        """
        # The model converts text -> vector
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def generate_batch_embeddings(self, texts, batch_size=32):
        """
        Generate embeddings for multiple texts efficiently.
        Much faster than doing them one-by-one!
        
        Args:
            texts: List of strings
            batch_size: How many to process at once
            
        Returns:
            numpy array of embeddings (one per text)
        """
        print(f"Generating embeddings for {len(texts)} texts...")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        
        print(f"✓ Generated {len(embeddings)} embeddings!")
        return embeddings
    
    def get_dimension(self):
        """Return the embedding dimension"""
        return self.dimension
    
    def compute_similarity(self, embedding1, embedding2):
        """
        Compute cosine similarity between two embeddings.
        Returns value between -1 and 1 (higher = more similar)
        
        Args:
            embedding1, embedding2: numpy arrays
            
        Returns:
            float: similarity score
        """
        # Cosine similarity formula
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        similarity = dot_product / (norm1 * norm2)
        return similarity


# Test when running directly
if __name__ == "__main__":
    print("Testing EmbeddingGenerator...\n")
    
    # Create generator
    gen = EmbeddingGenerator()
    
    # Test single embedding
    text1 = "The company's confidential financial report"
    emb1 = gen.generate_embedding(text1)
    print(f"\nText: '{text1}'")
    print(f"Embedding shape: {emb1.shape}")
    print(f"First 5 values: {emb1[:5]}")
    
    # Test similarity
    text2 = "Secret financial document"
    text3 = "Chocolate cake recipe"
    
    emb2 = gen.generate_embedding(text2)
    emb3 = gen.generate_embedding(text3)
    
    sim_12 = gen.compute_similarity(emb1, emb2)
    sim_13 = gen.compute_similarity(emb1, emb3)
    
    print(f"\nSimilarity Tests:")
    print(f"'{text1}' vs '{text2}': {sim_12:.3f} (should be HIGH)")
    print(f"'{text1}' vs '{text3}': {sim_13:.3f} (should be LOW)")
    
    # Test batch
    print("\nTesting batch generation...")
    texts = ["Document 1", "Document 2", "Document 3"]
    batch_embs = gen.generate_batch_embeddings(texts)
    print(f"✓ Generated {len(batch_embs)} embeddings in batch!")