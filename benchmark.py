#!/usr/bin/env python3
import time
import numpy as np
from src.encryption import EncryptionManager
from src.embeddings import EmbeddingGenerator
from src.cyborgdb_sim import CyborgDBClient
from src.rag import RAGOrchestrator

def benchmark():
    print("\n" + "="*70)
    print("INTELLIVAULT PERFORMANCE BENCHMARK")
    print("="*70)
    
    enc = EncryptionManager()
    emb = EmbeddingGenerator()
    db = CyborgDBClient(use_simulated=True)
    rag = RAGOrchestrator(enc, emb, db)
    
    queries = [
        "software license terms",
        "employee benefits",
        "financial performance",
        "security requirements",
        "compliance regulations"
    ] * 5  # 25 queries
    
    print(f"\nRunning {len(queries)} queries...\n")
    
    latencies = []
    for i, query in enumerate(queries, 1):
        start = time.time()
        result = rag.query(query, top_k=3)
        latency = time.time() - start
        latencies.append(latency)
        
        if i % 5 == 0:
            print(f"  Completed {i}/{len(queries)} queries...")
    
    latencies = np.array(latencies)
    
    print("\n" + "="*70)
    print("BENCHMARK RESULTS")
    print("="*70)
    print(f"\n📊 Query Latency:")
    print(f"  Mean:   {latencies.mean()*1000:.1f}ms")
    print(f"  Median: {np.median(latencies)*1000:.1f}ms")
    print(f"  P95:    {np.percentile(latencies, 95)*1000:.1f}ms")
    print(f"  P99:    {np.percentile(latencies, 99)*1000:.1f}ms")
    
    print(f"\n⚡ Throughput:")
    print(f"  Queries/second: {len(queries)/latencies.sum():.1f}")
    
    stats = db.get_stats()
    print(f"\n💾 Database:")
    print(f"  Total vectors: {stats['count']}")
    
    if latencies.mean() < 1.0:
        print(f"\n✅ EXCELLENT PERFORMANCE (<1s average)")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    benchmark()
