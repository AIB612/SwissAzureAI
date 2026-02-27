# 🐘 PostgreSQL pgvector Private Deployment

> Self-hosted RAG with full data sovereignty

---

## 🎯 Why Private Deployment?

| Concern | Solution |
|---------|----------|
| Data leaves Switzerland | ❌ Never with private deployment |
| Vendor lock-in | ✅ Open source stack |
| Cost control | ✅ Predictable infrastructure costs |
| Full audit trail | ✅ Complete control |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Private Infrastructure                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │  Ollama  │   │  PostgreSQL  │   │    MinIO     │        │
│  │  (LLM)   │   │  + pgvector  │   │  (Storage)   │        │
│  └────┬─────┘   └──────┬───────┘   └──────┬───────┘        │
│       │                │                   │                │
│       └────────────────┼───────────────────┘                │
│                        ▼                                    │
│               ┌────────────────┐                            │
│               │    FastAPI     │                            │
│               │   Application  │                            │
│               └────────────────┘                            │
│                        │                                    │
│                        ▼                                    │
│               ┌────────────────┐                            │
│               │     Nginx      │                            │
│               │   (Reverse)    │                            │
│               └────────────────┘                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: ragdb
      POSTGRES_USER: raguser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama:/root/.ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  app:
    build: ./app
    environment:
      DATABASE_URL: postgresql://raguser:${DB_PASSWORD}@postgres:5432/ragdb
      OLLAMA_HOST: http://ollama:11434
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - ollama

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD}
    volumes:
      - minio:/data
    ports:
      - "9000:9000"
      - "9001:9001"

volumes:
  pgdata:
  ollama:
  minio:
```

### 2. Initialize pgvector

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for similarity search
CREATE INDEX ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### 3. Python RAG Application

```python
# app/main.py
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import psycopg2
import ollama

app = FastAPI(title="Swiss Private RAG")

# Load embedding model
embedder = SentenceTransformer('BAAI/bge-small-en-v1.5')

@app.post("/index")
async def index_document(content: str, metadata: dict = None):
    """Index a document"""
    embedding = embedder.encode(content).tolist()
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (content, metadata, embedding) VALUES (%s, %s, %s)",
        (content, metadata, embedding)
    )
    conn.commit()
    return {"status": "indexed"}

@app.post("/query")
async def query(question: str, top_k: int = 3):
    """RAG query"""
    # 1. Embed question
    query_embedding = embedder.encode(question).tolist()
    
    # 2. Search similar documents
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT content, 1 - (embedding <=> %s::vector) as similarity
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (query_embedding, query_embedding, top_k))
    
    results = cur.fetchall()
    context = "\n\n".join([r[0] for r in results])
    
    # 3. Generate answer with Ollama
    response = ollama.chat(
        model='llama3',
        messages=[{
            'role': 'user',
            'content': f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        }]
    )
    
    return {
        "answer": response['message']['content'],
        "sources": [{"content": r[0], "score": r[1]} for r in results]
    }
```

---

## 🔧 Embedding Models (Local)

| Model | Size | Language |
|-------|------|----------|
| BAAI/bge-small-en-v1.5 | 130MB | English |
| BAAI/bge-m3 | 2.3GB | Multilingual |
| sentence-transformers/all-MiniLM-L6-v2 | 90MB | English |

---

## 🔒 Security Hardening

```yaml
# docker-compose.override.yml (production)
services:
  postgres:
    networks:
      - internal
    # No external ports exposed
    
  app:
    networks:
      - internal
      - external
    environment:
      - SSL_CERT_FILE=/certs/server.crt
      
networks:
  internal:
    internal: true
  external:
```

---

## 📊 Performance Tuning

```sql
-- PostgreSQL tuning for vector search
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';
ALTER SYSTEM SET maintenance_work_mem = '2GB';
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
```

---

## 📚 References

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Ollama](https://ollama.ai)
- [Sentence Transformers](https://www.sbert.net)
