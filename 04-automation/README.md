# ⚙️ Automation & Infrastructure as Code

> CI/CD, Terraform, Bicep for Swiss AI Deployments

---

## 🏗️ Infrastructure as Code

### Option 1: Terraform (Multi-cloud)

```hcl
# main.tf - Azure Switzerland North RAG Infrastructure

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

# Variables
variable "project_name" {
  default = "swiss-rag"
}

variable "location" {
  default = "switzerlandnorth"
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}-prod"
  location = var.location
}

# Azure OpenAI Service
resource "azurerm_cognitive_account" "openai" {
  name                = "oai-${var.project_name}"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "OpenAI"
  sku_name            = "S0"

  identity {
    type = "SystemAssigned"
  }
}

# Azure AI Search
resource "azurerm_search_service" "main" {
  name                = "search-${var.project_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  sku                 = "standard"

  identity {
    type = "SystemAssigned"
  }
}

# Storage Account (LRS for Switzerland only)
resource "azurerm_storage_account" "main" {
  name                     = "st${replace(var.project_name, "-", "")}prod"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"  # Local only - no geo-replication
  min_tls_version          = "TLS1_2"

  blob_properties {
    delete_retention_policy {
      days = 30
    }
  }
}

# PostgreSQL Flexible Server (for pgvector)
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "psql-${var.project_name}"
  resource_group_name    = azurerm_resource_group.main.name
  location               = var.location
  version                = "16"
  administrator_login    = "ragadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2s_v3"

  high_availability {
    mode = "ZoneRedundant"
  }
}

# Enable pgvector extension
resource "azurerm_postgresql_flexible_server_configuration" "pgvector" {
  name      = "azure.extensions"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "vector"
}

# Key Vault
resource "azurerm_key_vault" "main" {
  name                = "kv-${var.project_name}"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  purge_protection_enabled = true
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "asp-${var.project_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "P1v3"
}

# App Service
resource "azurerm_linux_web_app" "main" {
  name                = "app-${var.project_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    "AZURE_OPENAI_ENDPOINT"    = azurerm_cognitive_account.openai.endpoint
    "AZURE_SEARCH_ENDPOINT"    = "https://${azurerm_search_service.main.name}.search.windows.net"
    "AZURE_STORAGE_ACCOUNT"    = azurerm_storage_account.main.name
  }
}

# Outputs
output "app_url" {
  value = azurerm_linux_web_app.main.default_hostname
}

output "openai_endpoint" {
  value = azurerm_cognitive_account.openai.endpoint
}
```

### Option 2: Bicep (Azure Native)

```bicep
// main.bicep - Azure Switzerland North RAG

@description('Project name')
param projectName string = 'swiss-rag'

@description('Location - Switzerland North only')
param location string = 'switzerlandnorth'

@secure()
param dbPassword string

// Resource Group scope
targetScope = 'resourceGroup'

// Azure OpenAI
resource openai 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: 'oai-${projectName}'
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: 'oai-${projectName}'
    publicNetworkAccess: 'Disabled'
  }
}

// Azure AI Search
resource search 'Microsoft.Search/searchServices@2023-11-01' = {
  name: 'search-${projectName}'
  location: location
  sku: {
    name: 'standard'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    hostingMode: 'default'
    publicNetworkAccess: 'disabled'
  }
}

// Storage Account
resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'st${replace(projectName, '-', '')}prod'
  location: location
  sku: {
    name: 'Standard_LRS'  // Local redundancy only
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

// Outputs
output openaiEndpoint string = openai.properties.endpoint
output searchEndpoint string = 'https://${search.name}.search.windows.net'
output storageEndpoint string = storage.properties.primaryEndpoints.blob
```

---

## 🔄 CI/CD Pipelines

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy Swiss RAG

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  AZURE_LOCATION: switzerlandnorth

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        
      - name: Terraform Init
        run: terraform init
        working-directory: ./infra
        
      - name: Terraform Validate
        run: terraform validate
        working-directory: ./infra
        
      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: ./infra
        env:
          ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          ARM_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
          
      - name: Deploy Infrastructure
        run: terraform apply -auto-approve tfplan
        working-directory: ./infra
        
      - name: Deploy Application
        uses: azure/webapps-deploy@v2
        with:
          app-name: app-swiss-rag
          package: ./app

  compliance-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Data Residency
        run: |
          # Verify all resources are in Switzerland North
          grep -r "switzerlandnorth" ./infra/*.tf
          if grep -r "westeurope\|eastus\|westus" ./infra/*.tf; then
            echo "ERROR: Non-Swiss regions detected!"
            exit 1
          fi
          
      - name: Security Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: './infra'
```

### Azure DevOps Pipeline

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  azureLocation: 'switzerlandnorth'

stages:
  - stage: Validate
    jobs:
      - job: TerraformValidate
        steps:
          - task: TerraformInstaller@0
            inputs:
              terraformVersion: 'latest'
              
          - task: TerraformTaskV4@4
            inputs:
              provider: 'azurerm'
              command: 'init'
              workingDirectory: '$(System.DefaultWorkingDirectory)/infra'
              
          - task: TerraformTaskV4@4
            inputs:
              provider: 'azurerm'
              command: 'validate'
              workingDirectory: '$(System.DefaultWorkingDirectory)/infra'

  - stage: Deploy
    dependsOn: Validate
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployInfra
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: TerraformTaskV4@4
                  inputs:
                    provider: 'azurerm'
                    command: 'apply'
                    workingDirectory: '$(System.DefaultWorkingDirectory)/infra'
```

---

## 🔒 Secrets Management

```bash
# Store secrets in Azure Key Vault
az keyvault secret set \
  --vault-name kv-swiss-rag \
  --name "db-password" \
  --value "$DB_PASSWORD"

az keyvault secret set \
  --vault-name kv-swiss-rag \
  --name "openai-key" \
  --value "$OPENAI_KEY"
```

---

## 📁 Project Structure

```
infra/
├── main.tf              # Main infrastructure
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── providers.tf         # Provider config
├── modules/
│   ├── networking/      # VNet, Private Endpoints
│   ├── security/        # Key Vault, RBAC
│   └── monitoring/      # Log Analytics, Alerts
└── environments/
    ├── dev.tfvars
    ├── staging.tfvars
    └── prod.tfvars
```
