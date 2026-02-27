# 🇨🇭 Swiss-Digital-Azure-EcoAI

**Enterprise AI Solutions for Swiss Data Compliance**

> By SherryAGI | Curated Open Source Projects for Azure RAG + Swiss Compliance

---

## 🎯 Ready-to-Use Open Source Projects

### 🔥 RAG Platforms (Self-hosted, Data Stays Local)

| Project | Stars | Description | Quick Start |
|---------|-------|-------------|-------------|
| **[RAGFlow](https://github.com/infiniflow/ragflow)** | 40k+ | Enterprise RAG engine with deep document understanding | `docker compose up -d` |
| **[Dify](https://github.com/langgenius/dify)** | 60k+ | Low-code LLM app platform with RAG | `docker compose up -d` |
| **[AnythingLLM](https://github.com/Mintplex-Labs/anything-llm)** | 30k+ | All-in-one desktop RAG app | Desktop installer |
| **[Quivr](https://github.com/QuivrHQ/quivr)** | 35k+ | Personal AI assistant with RAG | `docker compose up` |
| **[PrivateGPT](https://github.com/zylon-ai/private-gpt)** | 55k+ | 100% private RAG, no data leaves | `poetry install` |

### ☁️ Azure RAG (Microsoft Official)

| Project | Description | Deploy |
|---------|-------------|--------|
| **[azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo)** | Official Azure RAG sample (Python) | `azd up` |
| **[azure-search-openai-demo-java](https://github.com/Azure-Samples/azure-search-openai-demo-java)** | Java version | `azd up` |
| **[azure-search-openai-demo-csharp](https://github.com/Azure-Samples/azure-search-openai-demo-csharp)** | .NET version | `azd up` |
| **[chat-with-your-data-solution-accelerator](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator)** | Enterprise accelerator | `azd up` |

### 🐘 PostgreSQL + pgvector

| Project | Description | Link |
|---------|-------------|------|
| **[pgvector](https://github.com/pgvector/pgvector)** | Vector extension for PostgreSQL | Core extension |
| **[pgvector-python](https://github.com/pgvector/pgvector-python)** | Python client | `pip install pgvector` |
| **[pg_vectorize](https://github.com/tembo-io/pg_vectorize)** | Auto-vectorization for Postgres | Tembo extension |

---

## 🚀 Quick Start Commands

### RAGFlow (Recommended for Enterprise)

```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker
docker compose up -d
# Access: http://localhost:80
```

### Dify (Low-code Platform)

```bash
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker compose up -d
# Access: http://localhost/install
```

### Azure RAG (Switzerland North)

```bash
git clone https://github.com/Azure-Samples/azure-search-openai-demo
cd azure-search-openai-demo
azd auth login
azd env new swiss-rag
azd env set AZURE_LOCATION switzerlandnorth
azd up
```

### pgvector + Python

```bash
# Install pgvector extension
CREATE EXTENSION vector;

# Python
pip install pgvector psycopg2-binary sentence-transformers
```

```python
from pgvector.psycopg2 import register_vector
import psycopg2

conn = psycopg2.connect("postgresql://user:pass@localhost/db")
register_vector(conn)

# Create table
cur = conn.cursor()
cur.execute("CREATE TABLE docs (id serial, content text, embedding vector(384))")

# Insert with embedding
cur.execute("INSERT INTO docs (content, embedding) VALUES (%s, %s)", 
            ("Hello world", [0.1, 0.2, ...]))

# Similarity search
cur.execute("SELECT content FROM docs ORDER BY embedding <=> %s LIMIT 5", 
            ([0.1, 0.2, ...],))
```

---

## 📋 Swiss Compliance Resources

### FADP (Federal Act on Data Protection)

| Resource | Link |
|----------|------|
| Official Law Text | [fedlex.admin.ch/eli/cc/2022/491](https://www.fedlex.admin.ch/eli/cc/2022/491) |
| FDPIC Guidelines | [edoeb.admin.ch](https://www.edoeb.admin.ch/edoeb/en/home.html) |
| FADP Summary (EN) | [kpmg.com/ch/fadp](https://kpmg.com/ch/en/home/insights/2022/09/new-swiss-data-protection-act.html) |

### FINMA (Financial Services)

| Resource | Link |
|----------|------|
| FINMA Circulars | [finma.ch/circulars](https://www.finma.ch/en/documentation/circulars/) |
| Operational Risk | Circular 2023/1 |
| Outsourcing | Circular 2018/3 |

### Azure Switzerland

| Resource | Link |
|----------|------|
| Azure Switzerland North | [azure.microsoft.com/regions](https://azure.microsoft.com/en-us/explore/global-infrastructure/geographies/#geographies) |
| Azure Compliance | [azure.microsoft.com/compliance](https://azure.microsoft.com/en-us/explore/trusted-cloud/compliance/) |
| Data Residency | [microsoft.com/trust-center](https://www.microsoft.com/en-us/trust-center/privacy/data-residency) |

---

## 🏗️ Architecture Patterns

### Pattern 1: Full Azure (Switzerland North)

```
Azure OpenAI ─── Azure AI Search ─── Azure Blob Storage
      │                 │
      └────── App Service (Python) ──────┘
```

**Use:** General enterprise, non-banking

### Pattern 2: Self-hosted (pgvector)

```
Ollama (LLM) ─── PostgreSQL + pgvector ─── MinIO
      │                   │
      └────── FastAPI Application ──────┘
```

**Use:** Banking, full data control, FINMA compliance

### Pattern 3: Hybrid

```
Azure OpenAI (no data stored) ◄──► On-prem PostgreSQL (customer data)
```

**Use:** Banks needing Azure AI but strict data residency

---

## 📁 Project Structure

```
SwissDigitalAzureEcoAI/
├── 01-azure-rag/              # Azure deployment guides
├── 02-pgvector-private/       # Self-hosted RAG setup
├── 03-compliance/             # FADP, GDPR, SOC2 checklists
├── 04-automation/             # Terraform, CI/CD templates
└── 05-reference-architecture/ # Enterprise patterns
```

---

## 📜 License

MIT License - SherryAGI

---

<div align="center">

**🇨🇭 Built for Swiss Enterprise AI Compliance**

[RAGFlow](https://github.com/infiniflow/ragflow) ·
[Dify](https://github.com/langgenius/dify) ·
[Azure RAG Demo](https://github.com/Azure-Samples/azure-search-openai-demo) ·
[pgvector](https://github.com/pgvector/pgvector)

</div>
