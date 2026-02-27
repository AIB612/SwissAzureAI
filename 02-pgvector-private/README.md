# 🐘 PostgreSQL pgvector Private Deployment

> Self-hosted RAG with full data sovereignty

---

## 🚀 Open Source Projects

### Core: pgvector

**GitHub:** https://github.com/pgvector/pgvector

```bash
# Docker (easiest)
docker run -d --name pgvector \
  -e POSTGRES_PASSWORD=mysecret \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

### RAG Platforms (Self-hosted)

| Project | GitHub | Quick Start |
|---------|--------|-------------|
| **RAGFlow** | https://github.com/infiniflow/ragflow | `docker compose up -d` |
| **Dify** | https://github.com/langgenius/dify | `docker compose up -d` |
| **PrivateGPT** | https://github.com/zylon-ai/private-gpt | `poetry install && make run` |
| **Quivr** | https://github.com/QuivrHQ/quivr | `docker compose up` |
| **AnythingLLM** | https://github.com/Mintplex-Labs/anything-llm | Desktop app |

---

## 🔥 RAGFlow (Recommended)

**GitHub:** https://github.com/infiniflow/ragflow

```bash
# Clone
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker

# Set vm.max_map_count (required)
sudo sysctl -w vm.max_map_count=262144

# Start
docker compose up -d

# Access: http://localhost:80
```

**Features:**
- ✅ Deep document understanding (PDF, DOCX, images)
- ✅ Multiple chunking strategies
- ✅ Built-in vector database
- ✅ Agent capabilities
- ✅ API access

---

## 🎨 Dify (Low-code)

**GitHub:** https://github.com/langgenius/dify

```bash
# Clone
git clone https://github.com/langgenius/dify.git
cd dify/docker

# Configure
cp .env.example .env

# Start
docker compose up -d

# Access: http://localhost/install
```

**Features:**
- ✅ Visual workflow builder
- ✅ RAG pipeline
- ✅ 100+ model integrations
- ✅ API & SDK

---

## 🔒 PrivateGPT (100% Offline)

**GitHub:** https://github.com/zylon-ai/private-gpt

```bash
# Clone
git clone https://github.com/zylon-ai/private-gpt.git
cd private-gpt

# Install
poetry install --extras "ui llms-llama-cpp embeddings-huggingface vector-stores-qdrant"

# Download models
poetry run python scripts/setup

# Run
make run

# Access: http://localhost:8001
```

**Features:**
- ✅ 100% offline capable
- ✅ No data leaves your machine
- ✅ Local LLM (Llama, Mistral)
- ✅ Local embeddings

---

## 🐘 pgvector Direct Usage

### Installation

```sql
-- Enable extension
CREATE EXTENSION vector;

-- Create table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding vector(384)
);

-- Create index
CREATE INDEX ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### Python Client

**GitHub:** https://github.com/pgvector/pgvector-python

```bash
pip install pgvector psycopg2-binary sentence-transformers
```

```python
import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

# Connect
conn = psycopg2.connect("postgresql://user:pass@localhost/ragdb")
register_vector(conn)
cur = conn.cursor()

# Load embedding model
model = SentenceTransformer('BAAI/bge-small-en-v1.5')

# Index document
text = "Company policy: Annual leave is 25 days."
embedding = model.encode(text).tolist()
cur.execute(
    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
    (text, embedding)
)
conn.commit()

# Search
query = "How many vacation days?"
query_embedding = model.encode(query).tolist()
cur.execute("""
    SELECT content, 1 - (embedding <=> %s::vector) as similarity
    FROM documents
    ORDER BY embedding <=> %s::vector
    LIMIT 5
""", (query_embedding, query_embedding))

for row in cur.fetchall():
    print(f"{row[1]:.3f}: {row[0]}")
```

---

## 🏠 Local LLM Options

| Project | GitHub | Description |
|---------|--------|-------------|
| **Ollama** | https://github.com/ollama/ollama | Easiest local LLM |
| **vLLM** | https://github.com/vllm-project/vllm | High-performance inference |
| **llama.cpp** | https://github.com/ggerganov/llama.cpp | CPU inference |
| **LocalAI** | https://github.com/mudler/LocalAI | OpenAI-compatible API |

### Ollama Quick Start

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Run model
ollama run llama3

# API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Hello!"
}'
```

---

## 📚 Documentation

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [RAGFlow Docs](https://ragflow.io/docs/dev/)
- [Dify Docs](https://docs.dify.ai/)
- [PrivateGPT Docs](https://docs.privategpt.dev/)
- [Ollama Docs](https://ollama.com/)
