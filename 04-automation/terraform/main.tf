# main.tf - Azure RAG Infrastructure for Switzerland North
# Deploy: terraform init && terraform apply

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

# Variables
variable "project_name" {
  description = "Project name prefix"
  default     = "swissrag"
}

variable "location" {
  description = "Azure region - Switzerland North for data residency"
  default     = "switzerlandnorth"
}

variable "db_password" {
  description = "PostgreSQL admin password"
  sensitive   = true
}

# Data
data "azurerm_client_config" "current" {}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}"
  location = var.location

  tags = {
    project     = var.project_name
    environment = "production"
    compliance  = "FADP"
  }
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

  tags = azurerm_resource_group.main.tags
}

# Azure AI Search
resource "azurerm_search_service" "main" {
  name                = "search-${var.project_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  sku                 = "basic"

  identity {
    type = "SystemAssigned"
  }

  tags = azurerm_resource_group.main.tags
}

# Storage Account (LRS - no geo-replication for data residency)
resource "azurerm_storage_account" "main" {
  name                     = "st${replace(var.project_name, "-", "")}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"  # Local redundancy only
  min_tls_version          = "TLS1_2"

  blob_properties {
    delete_retention_policy {
      days = 30
    }
  }

  tags = azurerm_resource_group.main.tags
}

# Blob Container
resource "azurerm_storage_container" "documents" {
  name                  = "documents"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "psql-${var.project_name}"
  resource_group_name    = azurerm_resource_group.main.name
  location               = var.location
  version                = "16"
  administrator_login    = "ragadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2s_v3"

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false  # Data residency

  tags = azurerm_resource_group.main.tags
}

# Enable pgvector extension
resource "azurerm_postgresql_flexible_server_configuration" "pgvector" {
  name      = "azure.extensions"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "vector"
}

# PostgreSQL Database
resource "azurerm_postgresql_flexible_server_database" "ragdb" {
  name      = "ragdb"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Key Vault
resource "azurerm_key_vault" "main" {
  name                = "kv-${var.project_name}"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  purge_protection_enabled   = true
  soft_delete_retention_days = 7

  tags = azurerm_resource_group.main.tags
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "asp-${var.project_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "B1"

  tags = azurerm_resource_group.main.tags
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
    "AZURE_OPENAI_ENDPOINT"            = azurerm_cognitive_account.openai.endpoint
    "AZURE_OPENAI_DEPLOYMENT"          = "gpt-4"
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT" = "text-embedding-ada-002"
    "AZURE_SEARCH_ENDPOINT"            = "https://${azurerm_search_service.main.name}.search.windows.net"
    "AZURE_STORAGE_ACCOUNT"            = azurerm_storage_account.main.name
    "POSTGRESQL_HOST"                  = azurerm_postgresql_flexible_server.main.fqdn
    "POSTGRESQL_DATABASE"              = "ragdb"
  }

  https_only = true

  tags = azurerm_resource_group.main.tags
}

# Outputs
output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "openai_endpoint" {
  value = azurerm_cognitive_account.openai.endpoint
}

output "search_endpoint" {
  value = "https://${azurerm_search_service.main.name}.search.windows.net"
}

output "storage_account_name" {
  value = azurerm_storage_account.main.name
}

output "postgresql_host" {
  value = azurerm_postgresql_flexible_server.main.fqdn
}

output "app_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}
