# 🇨🇭 SwissAzureAI

**Enterprise AI & Digital Transformation with Microsoft Ecosystem**

> By SherryAGI | Azure + M365 + Swiss Compliance

---

## 📁 Project Structure

```
SwissAzureAI/
├── 00-microsoft-ecosystem/  # 微软开源项目合集
├── 01-azure-rag/            # Azure RAG 实现
├── 02-pgvector-private/     # 私有部署 (银行/FINMA)
├── 03-compliance/           # FADP, FINMA 检查清单
└── 04-automation/           # Terraform, CI/CD
```

---

## 🎯 Core Reference

### Azure RAG Demo (Microsoft Official)

**GitHub:** https://github.com/Azure-Samples/azure-search-openai-demo

```bash
git clone https://github.com/Azure-Samples/azure-search-openai-demo
cd azure-search-openai-demo
azd env set AZURE_LOCATION switzerlandnorth
azd up
```

---

## 🏢 Microsoft Ecosystem Highlights

| Category | Key Projects |
|----------|--------------|
| **AI** | [semantic-kernel](https://github.com/microsoft/semantic-kernel), [autogen](https://github.com/microsoft/autogen) |
| **M365** | [PnP PowerShell](https://github.com/pnp/powershell), [CLI for M365](https://github.com/pnp/cli-microsoft365) |
| **DevOps** | [Bicep](https://github.com/Azure/bicep), [ALZ](https://github.com/Azure/ALZ-Bicep) |
| **Data** | [Fabric Samples](https://github.com/microsoft/fabric-samples), [SynapseML](https://github.com/microsoft/SynapseML) |

👉 See [00-microsoft-ecosystem/README.md](./00-microsoft-ecosystem/README.md) for full list

---

## 🚀 Quick Start

### Azure RAG
```bash
cd 01-azure-rag/infra
az deployment group create -g rg-swiss-rag --template-file main.bicep
```

### Private Deployment
```bash
cd 02-pgvector-private/docker
docker compose up -d
```

### M365 Automation
```powershell
Install-Module PnP.PowerShell
Connect-PnPOnline -Url https://contoso.sharepoint.com -Interactive
```

---

## 📋 Swiss Compliance

| Requirement | Implementation |
|-------------|----------------|
| Data Residency | Azure Switzerland North |
| FADP | [Checklist](./03-compliance/FADP_CHECKLIST.md) |
| FINMA | [Checklist](./03-compliance/FINMA_CHECKLIST.md) |

---

## 📚 Resources

- [Microsoft Learn](https://learn.microsoft.com)
- [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/)
- [PnP Community](https://pnp.github.io)

---

## 📜 License

MIT License - SherryAGI
