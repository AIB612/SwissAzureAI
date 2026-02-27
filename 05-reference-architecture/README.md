# 🏛️ Reference Architecture

> Enterprise AI Architecture - Open Source References

---

## 📚 Official Architecture References

### Microsoft Azure

| Resource | Link |
|----------|------|
| **Azure OpenAI Landing Zone** | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/azure-openai-baseline-landing-zone |
| **RAG Pattern Guide** | https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview |
| **Azure Well-Architected** | https://learn.microsoft.com/en-us/azure/well-architected/ |
| **AI Architecture Center** | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/ |

### Open Source RAG Architectures

| Project | Architecture Docs |
|---------|-------------------|
| **RAGFlow** | https://ragflow.io/docs/dev/ |
| **Dify** | https://docs.dify.ai/getting-started/readme |
| **LangChain** | https://python.langchain.com/docs/tutorials/rag/ |
| **LlamaIndex** | https://docs.llamaindex.ai/en/stable/ |

---

## 🏗️ Architecture Patterns

### Pattern 1: Azure Native

**Reference:** https://github.com/Azure-Samples/azure-search-openai-demo

```
┌─────────────────────────────────────────────────────────────┐
│                 Azure Switzerland North                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User ──► App Service ──► Azure OpenAI                     │
│                │                                             │
│                ▼                                             │
│         Azure AI Search ◄── Azure Blob Storage              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Deploy:**
```bash
git clone https://github.com/Azure-Samples/azure-search-openai-demo
cd azure-search-openai-demo
azd env set AZURE_LOCATION switzerlandnorth
azd up
```

### Pattern 2: Self-hosted (RAGFlow)

**Reference:** https://github.com/infiniflow/ragflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User ──► Nginx ──► RAGFlow API ──► Ollama (LLM)          │
│                          │                                   │
│                          ▼                                   │
│                    Elasticsearch ◄── MinIO                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Deploy:**
```bash
git clone https://github.com/infiniflow/ragflow
cd ragflow/docker
docker compose up -d
```

### Pattern 3: pgvector + FastAPI

**Reference:** https://github.com/pgvector/pgvector

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes / Docker                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User ──► FastAPI ──► Ollama (LLM)                        │
│                │                                             │
│                ▼                                             │
│         PostgreSQL + pgvector ◄── S3/MinIO                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Deploy:**
```bash
# docker-compose.yml
docker compose up -d
```

---

## 🔗 Open Source Architecture Tools

| Tool | GitHub | Description |
|------|--------|-------------|
| **Diagrams** | https://github.com/mingrammer/diagrams | Architecture as code |
| **Structurizr** | https://github.com/structurizr/dsl | C4 model diagrams |
| **Mermaid** | https://github.com/mermaid-js/mermaid | Markdown diagrams |
| **Draw.io** | https://github.com/jgraph/drawio | Diagram editor |

### Diagrams as Code Example

```python
# pip install diagrams
from diagrams import Diagram
from diagrams.azure.compute import AppServices
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.ai import CognitiveServices

with Diagram("Swiss RAG Architecture", show=False):
    user = AppServices("App Service")
    openai = CognitiveServices("Azure OpenAI")
    db = DatabaseForPostgresqlServers("PostgreSQL")
    
    user >> openai >> db
```

---

## 📊 Comparison Matrix

| Feature | Azure Native | RAGFlow | pgvector |
|---------|--------------|---------|----------|
| Setup | `azd up` | `docker compose` | Manual |
| Data Residency | Switzerland North | Self-hosted | Self-hosted |
| Cost | Pay-as-you-go | Infrastructure only | Infrastructure only |
| Scalability | Auto | Manual | Manual |
| Maintenance | Managed | Self | Self |
| FINMA Ready | Review needed | ✅ Full control | ✅ Full control |

---

## 📚 Learning Resources

### Courses

| Course | Platform | Link |
|--------|----------|------|
| RAG with LangChain | DeepLearning.AI | https://www.deeplearning.ai/short-courses/ |
| Azure AI Fundamentals | Microsoft Learn | https://learn.microsoft.com/en-us/training/paths/get-started-with-artificial-intelligence-on-azure/ |
| Vector Databases | Pinecone | https://www.pinecone.io/learn/ |

### Books

| Title | Link |
|-------|------|
| Building LLM Apps | https://www.oreilly.com/library/view/building-llm-apps/9781835462317/ |
| Designing Data-Intensive Applications | https://dataintensive.net/ |

---

## 🔗 Community

| Community | Link |
|-----------|------|
| RAGFlow Discord | https://discord.gg/NjYzJD3GM3 |
| Dify Discord | https://discord.gg/FngNHpbcY7 |
| LangChain Discord | https://discord.gg/langchain |
| Azure AI Community | https://techcommunity.microsoft.com/t5/azure-ai/ct-p/AzureAI |
