# 🔍 Azure RAG Implementation

> Based on Microsoft azure-search-openai-demo

---

## 🚀 Official Microsoft Project

**GitHub:** https://github.com/Azure-Samples/azure-search-openai-demo

### Deploy to Switzerland North

```bash
# Clone official demo
git clone https://github.com/Azure-Samples/azure-search-openai-demo
cd azure-search-openai-demo

# Configure for Switzerland
azd auth login
azd env new swiss-rag-prod
azd env set AZURE_LOCATION switzerlandnorth
azd env set AZURE_OPENAI_LOCATION switzerlandnorth

# Deploy
azd up
```

---

## 📦 Other Language Versions

| Language | GitHub |
|----------|--------|
| Python | https://github.com/Azure-Samples/azure-search-openai-demo |
| Java | https://github.com/Azure-Samples/azure-search-openai-demo-java |
| C# | https://github.com/Azure-Samples/azure-search-openai-demo-csharp |
| JavaScript | https://github.com/Azure-Samples/azure-search-openai-javascript |

---

## 📁 This Repo's Files

| File | Description |
|------|-------------|
| `infra/main.bicep` | Simplified Bicep template for Switzerland North |
| `app/main.py` | Standalone FastAPI RAG application |
| `app/.env.example` | Environment variables template |

---

## 📚 Microsoft Documentation

- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Search](https://learn.microsoft.com/azure/search/)
- [RAG Pattern](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview)
- [Landing Zone Architecture](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/azure-openai-baseline-landing-zone)
