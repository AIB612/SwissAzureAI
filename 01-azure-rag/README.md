# 🔍 Azure RAG Implementation

> Azure AI Search + Azure OpenAI in Switzerland North

---

## 📋 Prerequisites

- Azure Subscription with Switzerland North access
- Azure OpenAI Service approved
- Azure CLI installed

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────┐
│  Azure App      │
│  Service        │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌───────────┐
│Azure  │  │Azure AI   │
│OpenAI │  │Search     │
└───────┘  └─────┬─────┘
                 │
                 ▼
          ┌───────────┐
          │Azure Blob │
          │Storage    │
          └───────────┘
```

---

## 🚀 Quick Start

### 1. Clone Azure Sample

```bash
git clone https://github.com/Azure-Samples/azure-search-openai-demo
cd azure-search-openai-demo
```

### 2. Configure for Switzerland North

```bash
# Set environment
azd env new swiss-rag-prod

# Configure region
azd env set AZURE_LOCATION switzerlandnorth
azd env set AZURE_OPENAI_LOCATION switzerlandnorth
```

### 3. Deploy

```bash
azd auth login
azd up
```

---

## 📁 Files

| File | Description |
|------|-------------|
| [infra/](./infra/) | Bicep/Terraform templates |
| [app/](./app/) | Python application code |
| [data/](./data/) | Sample documents |

---

## ⚙️ Configuration

### Environment Variables

```env
AZURE_LOCATION=switzerlandnorth
AZURE_OPENAI_SERVICE=your-openai-service
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_SEARCH_SERVICE=your-search-service
AZURE_SEARCH_INDEX=your-index
AZURE_STORAGE_ACCOUNT=your-storage
```

### Switzerland North Available Models

| Model | Availability |
|-------|--------------|
| gpt-4 | ✅ Available |
| gpt-4-turbo | ✅ Available |
| gpt-35-turbo | ✅ Available |
| text-embedding-ada-002 | ✅ Available |

---

## 🔒 Security Best Practices

1. **Private Endpoints** - No public internet exposure
2. **Managed Identity** - No credentials in code
3. **Key Vault** - Secrets management
4. **Network Isolation** - VNet integration

---

## 📚 References

- [Azure OpenAI Switzerland North](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)
- [Azure Search OpenAI Demo](https://github.com/Azure-Samples/azure-search-openai-demo)
- [Azure OpenAI Landing Zone](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/azure-openai-baseline-landing-zone)
