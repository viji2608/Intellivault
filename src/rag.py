from typing import List, Dict, Any
import numpy as np

class RAGOrchestrator:
    """Complete RAG orchestration system"""
    
    def __init__(self, encryption_manager, embedding_generator, 
                 db_client, llm_client=None):
        self.enc = encryption_manager
        self.emb = embedding_generator
        self.db = db_client
        self.llm = llm_client
        
        print("✓ RAG Orchestrator initialized")
    
    def query(self, query_text: str, top_k: int = 5) -> Dict[str, Any]:
        """Execute complete RAG query"""
        print(f"\nQUERY: {query_text}")
        
        # Generate and encrypt query
        query_embedding = self.emb.generate_embedding(query_text)
        encrypted_query = self.enc.encrypt_vector(query_embedding)
        
        # Search
        results = self.db.encrypted_search(encrypted_query, top_k=top_k)
        
        # Decrypt and rank
        decrypted_results = []
        for result in results:
            decrypted_vec = self.enc.decrypt_vector(result['vector'])
            similarity = self._compute_similarity(query_embedding, decrypted_vec)
            
            decrypted_results.append({
                'id': result['id'],
                'similarity': float(similarity),
                'metadata': result['metadata'],
                'content': result['metadata'].get('content', '')
            })
        
        decrypted_results.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Generate answer
        answer = self._generate_answer(query_text, decrypted_results)
        
        return {
            'query': query_text,
            'answer': answer,
            'sources': decrypted_results,
            'num_sources': len(decrypted_results),
            'top_similarity': decrypted_results[0]['similarity'] if decrypted_results else 0.0
        }
    
    def _compute_similarity(self, vec1, vec2):
        """Cosine similarity"""
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot / (norm1 * norm2) if norm1 and norm2 else 0.0
    
    def _generate_answer(self, query: str, results: List[Dict]) -> str:
        """Generate answer from results"""
        if not results:
            return "No relevant information found."
        
        top = results[0]
        doc_id = top['metadata'].get('doc_id', 'unknown')
        similarity = top['similarity']
        
        return (
            f"Based on '{doc_id}' (relevance: {similarity:.1%}):\n\n"
            f"{top['content'][:500]}"
        )
