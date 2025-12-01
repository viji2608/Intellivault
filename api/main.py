from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.encryption import EncryptionManager
from src.embeddings import EmbeddingGenerator
from src.cyborgdb_sim import CyborgDBClient
from src.rag import RAGOrchestrator

app = FastAPI(title="IntelliVault API")

# FIXED: Allow all origins for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

rag = None

@app.on_event("startup")
async def startup():
    global rag
    enc = EncryptionManager()
    emb = EmbeddingGenerator()
    db = CyborgDBClient(use_simulated=True)
    rag = RAGOrchestrator(enc, emb, db)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@app.get("/")
def root():
    return {"message": "IntelliVault API", "status": "running"}

@app.post("/query")
def query_kb(request: QueryRequest):
    response = rag.query(request.query, top_k=request.top_k)
    return response

@app.get("/stats")
def get_stats():
    stats = rag.db.get_stats()
    return stats if stats else {"error": "No stats"}

@app.get("/health")
def health():
    return {"status": "healthy", "encryption": "active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
