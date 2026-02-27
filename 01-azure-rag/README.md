# 🔍 Azure RAG Implementation

> Azure AI Search + Azure OpenAI in Switzerland North

---

## 🚀 Official Microsoft Open Source Projects

### Primary: azure-search-openai-demo

**GitHub:** https://github.com/Azure-Samples/azure-search-openai-demo

```bash
# Clone
git clone https://github.com/Azure-Samples/azure-search-openai-demo
cd azure-search-openai-demo

# Deploy to Switzerland North
azd auth login
azd env new swiss-rag-prod
azd env set AZURE_LOCATION switzerlandnorth
azd env set AZURE_OPENAI_LOCATION switzerlandnorth
azd up
```

**Features:**
- ✅ Chat interface with citations
- ✅ Document ingestion (PDF, DOCX, etc.)
- ✅ Azure AI Search integration
- ✅ Azure OpenAI GPT-4
- ✅ Python backend

---

## 📦 Other Azure RAG Samples

| Project | Language | Link |
|---------|----------|------|
| azure-search-openai-demo | Python | [GitHub](https://github.com/Azure-Samples/azure-search-openai-demo) |
| azure-search-openai-demo-java | Java | [GitHub](https://github.com/Azure-Samples/azure-search-openai-demo-java) |
| azure-search-openai-demo-csharp | C# | [GitHub](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) |
| azure-search-openai-javascript | JavaScript | [GitHub](https://github.com/Azure-Samples/azure-search-openai-javascript) |
| chat-with-your-data-solution-accelerator | Python | [GitHub](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator) |

---

## ⚙️ Switzerland North Configuration

```bash
# Required environment variables
export AZURE_LOCATION=switzerlandnorth
export AZURE_OPENAI_LOCATION=switzerlandnorth
export AZURE_OPENAI_RESOURCE_GROUP=rg-swiss-rag
export AZURE_OPENAI_SERVICE=oai-swiss-rag
export AZURE_SEARCH_SERVICE=search-swiss-rag
```

### Available Services in Switzerland North

| Service | Status |
|---------|--------|
| Azure OpenAI | ✅ Available |
| Azure AI Search | ✅ Available |
| Azure Blob Storage | ✅ Available |
| Azure PostgreSQL | ✅ Available |
| Azure App Service | ✅ Available |
| Azure Container Apps | ✅ Available |

---

## 📚 Documentation

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure AI Search Documentation](https://learn.microsoft.com/en-us/azure/search/)
- [RAG Pattern Guide](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Azure OpenAI Landing Zone](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/azure-openai-baseline-landing-zone)
