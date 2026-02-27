# 🐘 PostgreSQL pgvector Private Deployment

> Self-hosted alternative for full data control (FINMA/Banking)

---

## 🎯 When to Use

| Scenario | Recommendation |
|----------|----------------|
| General Enterprise | Use Azure (01-azure-rag) |
| Banking / FINMA | Use this private deployment |
| Full data sovereignty | Use this private deployment |

---

## 🚀 Quick Start

```bash
cd docker
docker compose up -d

# Access: http://localhost:8000
```

---

## 📁 Files

| File | Description |
|------|-------------|
| `docker/docker-compose.yml` | Full stack (PostgreSQL + Ollama + App) |
| `docker/init.sql` | Database initialization |
| `app/main.py` | FastAPI RAG application |
| `app/Dockerfile` | Container image |

---

## 🏗️ Architecture

```
PostgreSQL + pgvector ─── FastAPI App ─── Ollama (Local LLM)
         │
      MinIO (Storage)
```

All components run locally. No data leaves your infrastructure.

---

## 📚 Resources

- [pgvector](https://github.com/pgvector/pgvector) - PostgreSQL vector extension
- [Ollama](https://ollama.com) - Local LLM runtime
- [Azure PostgreSQL](https://learn.microsoft.com/azure/postgresql/) - Managed option
