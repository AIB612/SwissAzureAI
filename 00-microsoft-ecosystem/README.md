# 🏢 Microsoft Ecosystem - Open Source Projects

> 数字化转型常用的微软开源项目

---

## 🤖 AI & Machine Learning

| Project | GitHub | Description |
|---------|--------|-------------|
| **azure-search-openai-demo** | https://github.com/Azure-Samples/azure-search-openai-demo | RAG 企业搜索 |
| **semantic-kernel** | https://github.com/microsoft/semantic-kernel | AI 编排框架 |
| **autogen** | https://github.com/microsoft/autogen | 多 Agent 框架 |
| **guidance** | https://github.com/guidance-ai/guidance | LLM 控制语言 |
| **JARVIS** | https://github.com/microsoft/JARVIS | AI 任务规划 |
| **DeepSpeed** | https://github.com/microsoft/DeepSpeed | 大模型训练优化 |
| **ONNX Runtime** | https://github.com/microsoft/onnxruntime | 模型推理引擎 |

---

## 📊 Power Platform & M365

| Project | GitHub | Description |
|---------|--------|-------------|
| **PnP PowerShell** | https://github.com/pnp/powershell | SharePoint/M365 自动化 |
| **PnP JS** | https://github.com/pnp/pnpjs | SharePoint JavaScript 库 |
| **PnP Core SDK** | https://github.com/pnp/pnpcore | M365 .NET SDK |
| **CLI for M365** | https://github.com/pnp/cli-microsoft365 | M365 命令行工具 |
| **sp-dev-fx-webparts** | https://github.com/pnp/sp-dev-fx-webparts | SPFx Web Parts 示例 |
| **List Formatting** | https://github.com/pnp/List-Formatting | SharePoint 列表格式化 |
| **Power Platform Samples** | https://github.com/pnp/powerplatform-samples | Power Apps/Automate 示例 |

---

## 🔧 DevOps & Infrastructure

| Project | GitHub | Description |
|---------|--------|-------------|
| **Bicep** | https://github.com/Azure/bicep | Azure IaC 语言 |
| **Azure CLI** | https://github.com/Azure/azure-cli | Azure 命令行 |
| **Terraform Azure** | https://github.com/hashicorp/terraform-provider-azurerm | Terraform Azure Provider |
| **Azure Landing Zones** | https://github.com/Azure/ALZ-Bicep | 企业级 Azure 架构 |
| **Azure Verified Modules** | https://github.com/Azure/terraform-azurerm-avm-template | 官方 Terraform 模块 |

---

## 📈 Data & Analytics

| Project | GitHub | Description |
|---------|--------|-------------|
| **Synapse ML** | https://github.com/microsoft/SynapseML | Spark ML 库 |
| **Data Factory Templates** | https://github.com/Azure/Azure-DataFactory | ADF 模板 |
| **Fabric Samples** | https://github.com/microsoft/fabric-samples | Microsoft Fabric 示例 |
| **Power BI Samples** | https://github.com/microsoft/powerbi-desktop-samples | Power BI 示例 |

---

## 🔐 Security & Identity

| Project | GitHub | Description |
|---------|--------|-------------|
| **MSAL** | https://github.com/AzureAD/microsoft-authentication-library-for-js | 身份认证库 |
| **Entra Samples** | https://github.com/Azure-Samples/active-directory-aspnetcore-webapp-openidconnect-v2 | Entra ID 示例 |

---

## 🚀 Quick Start Commands

### PnP PowerShell (M365 自动化)
```powershell
Install-Module PnP.PowerShell
Connect-PnPOnline -Url https://contoso.sharepoint.com -Interactive
Get-PnPList
```

### CLI for M365
```bash
npm install -g @pnp/cli-microsoft365
m365 login
m365 spo site list
```

### Semantic Kernel (AI 编排)
```bash
pip install semantic-kernel
```

```python
import semantic_kernel as sk
kernel = sk.Kernel()
```

### AutoGen (多 Agent)
```bash
pip install pyautogen
```

```python
from autogen import AssistantAgent, UserProxyAgent
assistant = AssistantAgent("assistant")
```

---

## 📚 Learning Resources

| Resource | Link |
|----------|------|
| Microsoft Learn | https://learn.microsoft.com |
| Azure Architecture Center | https://learn.microsoft.com/azure/architecture/ |
| PnP Community | https://pnp.github.io |
| Power Platform Docs | https://learn.microsoft.com/power-platform/ |
