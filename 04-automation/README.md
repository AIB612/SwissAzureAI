# ⚙️ Automation & Infrastructure as Code

> Terraform, Bicep, CI/CD - Open Source Templates

---

## 🚀 Open Source IaC Projects

### Azure RAG Infrastructure

| Project | GitHub | Description |
|---------|--------|-------------|
| **azure-search-openai-demo** | https://github.com/Azure-Samples/azure-search-openai-demo/tree/main/infra | Official Bicep templates |
| **Azure Landing Zones** | https://github.com/Azure/ALZ-Bicep | Enterprise-scale Bicep |
| **Azure Verified Modules** | https://github.com/Azure/terraform-azurerm-avm-template | Terraform modules |

### Terraform Modules

| Module | Registry | Description |
|--------|----------|-------------|
| **azurerm_cognitive_account** | https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account | Azure OpenAI |
| **azurerm_search_service** | https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/search_service | AI Search |
| **azurerm_postgresql_flexible_server** | https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/postgresql_flexible_server | PostgreSQL |

---

## 📦 Quick Start Templates

### Terraform - Azure RAG (Switzerland North)

```hcl
# main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "location" {
  default = "switzerlandnorth"
}

resource "azurerm_resource_group" "main" {
  name     = "rg-swiss-rag"
  location = var.location
}

resource "azurerm_cognitive_account" "openai" {
  name                = "oai-swiss-rag"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "OpenAI"
  sku_name            = "S0"
}

resource "azurerm_search_service" "main" {
  name                = "search-swiss-rag"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  sku                 = "standard"
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "psql-swiss-rag"
  resource_group_name    = azurerm_resource_group.main.name
  location               = var.location
  version                = "16"
  administrator_login    = "ragadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2s_v3"
}
```

```bash
# Deploy
terraform init
terraform plan
terraform apply
```

### Bicep - Azure RAG

```bicep
// main.bicep
param location string = 'switzerlandnorth'
param projectName string = 'swiss-rag'

resource openai 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: 'oai-${projectName}'
  location: location
  kind: 'OpenAI'
  sku: { name: 'S0' }
}

resource search 'Microsoft.Search/searchServices@2023-11-01' = {
  name: 'search-${projectName}'
  location: location
  sku: { name: 'standard' }
}
```

```bash
# Deploy
az deployment group create \
  --resource-group rg-swiss-rag \
  --template-file main.bicep
```

---

## 🔄 CI/CD Templates

### GitHub Actions

**Source:** https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/.github/workflows/

```yaml
# .github/workflows/deploy.yml
name: Deploy Swiss RAG

on:
  push:
    branches: [main]

env:
  AZURE_LOCATION: switzerlandnorth

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
          
      - name: Deploy Bicep
        uses: azure/arm-deploy@v1
        with:
          resourceGroupName: rg-swiss-rag
          template: ./infra/main.bicep
          parameters: location=switzerlandnorth
```

### Azure DevOps

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: Deploy
    jobs:
      - job: Terraform
        steps:
          - task: TerraformInstaller@0
            inputs:
              terraformVersion: 'latest'
          - task: TerraformTaskV4@4
            inputs:
              provider: 'azurerm'
              command: 'apply'
              workingDirectory: '$(System.DefaultWorkingDirectory)/infra'
```

---

## 🔧 Open Source CI/CD Tools

| Tool | GitHub | Description |
|------|--------|-------------|
| **GitHub Actions** | https://github.com/features/actions | CI/CD for GitHub |
| **Terraform** | https://github.com/hashicorp/terraform | IaC tool |
| **Bicep** | https://github.com/Azure/bicep | Azure IaC |
| **Pulumi** | https://github.com/pulumi/pulumi | Multi-cloud IaC |
| **OpenTofu** | https://github.com/opentofu/opentofu | Terraform fork |

---

## 📚 Documentation

- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Bicep Documentation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/)
- [GitHub Actions for Azure](https://github.com/Azure/actions)
- [Azure DevOps Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/)
