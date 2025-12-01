# IntelliVault Architecture

## System Overview┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACES                         │
├─────────────────────────────────────────────────────────────┤
│  CLI (query.py)  │  REST API (FastAPI)  │  Web UI (Future) │
└──────────────────┴──────────────────────┴───────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│                    RAG ORCHESTRATOR                          │
│  • Query processing   • Context assembly                     │
│  • Similarity ranking • Answer generation                    │
└─────────────────────────────────────────────────────────────┘
│
┌──────────────────┼──────────────────┐
▼                  ▼                  ▼
┌─────────────────┐  ┌──────────────┐  ┌──────────────────┐
│  ENCRYPTION     │  │  EMBEDDINGS  │  │  CYBORGDB        │
│  AES-256-GCM    │  │  Sentence    │  │  Encrypted       │
│  Client-side    │  │  Transformers│  │  Vector Search   │
└─────────────────┘  └──────────────┘  └──────────────────┘
│
▼
┌─────────────────┐
│   ENCRYPTED     │
│   STORAGE       │
│   (No plaintext)│
└─────────────────┘

## Data Flow

### Ingestion PipelineDocument → Parse → Chunk → Embed → Encrypt → CyborgDB
.txt      text    500w    384d    AES-256   encrypted

### Query PipelineQuestion → Embed → Encrypt → Search → Decrypt → Rank → Answer
text      384d    AES-256  CyborgDB ephemeral cosine  LLM

## Security Model

1. **Client-side Encryption**: All vectors encrypted before leaving client
2. **Zero Plaintext**: CyborgDB never sees unencrypted data
3. **Ephemeral Decryption**: Results decrypted only in secure memory
4. **Key Management**: AES keys stored separately, rotation supported

## Scalability

- **Current**: 3 documents, <1s queries
- **Tested**: 100 documents capability
- **Target**: 1M+ documents, <2s queries
- **Horizontal scaling**: Shard by department/tenant

## Technology Stack

- **Encryption**: pycryptodome (AES-256-GCM)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: CyborgDB (encrypted search)
- **API**: FastAPI + Uvicorn
- **Python**: 3.12+
