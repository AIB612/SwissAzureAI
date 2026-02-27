# 🇨🇭 Swiss-Digital-Azure-EcoAI

**Enterprise AI Solutions for Swiss Data Compliance**

> By SherryAGI | Azure RAG + Swiss Data Residency + FADP/GDPR Compliance

---

## 🎯 Based on Microsoft Official Project

### azure-search-openai-demo

**GitHub:** https://github.com/Azure-Samples/azure-search-openai-demo

Microsoft 官方 RAG 示例，支持 Switzerland North 部署。

```bash
# Clone
git clone https://github.com/Azure-Samples/azure-search-openai-demo
cd azure-search-openai-demo

# Deploy to Switzerland North
azd auth login
azd env new swiss-rag
azd env set AZURE_LOCATION switzerlandnorth
azd env set AZURE_OPENAI_LOCATION switzerlandnorth
azd up
```

**Features:**
- ✅ Chat interface with citations
- ✅ Document ingestion (PDF, DOCX, etc.)
- ✅ Azure AI Search + Azure OpenAI
- ✅ Python/Java/.NET/JavaScript versions
- ✅ Enterprise-ready architecture

---

## 📁 Project Structure

```
SwissAzureAI/
├── 01-azure-rag/              # Azure deployment (based on MS demo)
│   ├── infra/main.bicep       # Infrastructure as Code
│   └── app/main.py            # FastAPI application
├── 02-pgvector-private/       # Self-hosted alternative
│   ├── docker/                # Docker Compose stack
│   └── app/                   # Private RAG app
├── 03-compliance/             # FADP, FINMA checklists
└── 04-automation/             # Terraform, CI/CD
```

---

## 🚀 Quick Start

### Option 1: Use Microsoft Demo Directly

```bash
git clone https://github.com/Azure-Samples/azure-search-openai-demo
cd azure-search-openai-demo
azd env set AZURE_LOCATION switzerlandnorth
azd up
```

### Option 2: Use This Repo's Templates

```bash
# Azure (Bicep)
cd 01-azure-rag/infra
az deployment group create -g rg-swiss-rag --template-file main.bicep

# Private (Docker)
cd 02-pgvector-private/docker
docker compose up -d
```

---

## 📋 Swiss Compliance

| Requirement | Implementation |
|-------------|----------------|
| Data Residency | Azure Switzerland North |
| FADP | [Checklist](./03-compliance/FADP_CHECKLIST.md) |
| FINMA | [Checklist](./03-compliance/FINMA_CHECKLIST.md) |
| Encryption | AES-256 at rest, TLS 1.3 in transit |

---

## 🔗 Microsoft Resources

| Resource | Link |
|----------|------|
| Azure RAG Demo | https://github.com/Azure-Samples/azure-search-openai-demo |
| Azure OpenAI Docs | https://learn.microsoft.com/azure/ai-services/openai/ |
| Azure AI Search | https://learn.microsoft.com/azure/search/ |
| Landing Zone | https://learn.microsoft.com/azure/architecture/ai-ml/architecture/azure-openai-baseline-landing-zone |

---

## 📜 License

MIT License - SherryAGI

---

<div align="center">

**🇨🇭 Built for Swiss Enterprise AI Compliance**

Based on [azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo)

</div>
