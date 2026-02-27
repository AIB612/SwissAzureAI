// main.bicep - Azure RAG Infrastructure for Switzerland North
// Deploy: az deployment group create --resource-group rg-swiss-rag --template-file main.bicep

@description('Project name prefix')
param projectName string = 'swissrag'

@description('Location - Switzerland North for data residency')
param location string = 'switzerlandnorth'

@secure()
@description('PostgreSQL admin password')
param dbPassword string

// Resource Group scope
targetScope = 'resourceGroup'

// Azure OpenAI Service
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
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
}

// GPT-4 Deployment
resource gpt4Deployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openai
  name: 'gpt-4'
  sku: {
    name: 'Standard'
    capacity: 10
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4'
      version: '0613'
    }
  }
}

// Embedding Model Deployment
resource embeddingDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openai
  name: 'text-embedding-ada-002'
  sku: {
    name: 'Standard'
    capacity: 10
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'text-embedding-ada-002'
      version: '2'
    }
  }
  dependsOn: [gpt4Deployment]
}

// Azure AI Search
resource search 'Microsoft.Search/searchServices@2023-11-01' = {
  name: 'search-${projectName}'
  location: location
  sku: {
    name: 'basic'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    partitionCount: 1
    replicaCount: 1
  }
}

// Storage Account (LRS for Switzerland only - no geo-replication)
resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'st${projectName}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    accessTier: 'Hot'
  }
}

// Blob Container for documents
resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storage.name}/default/documents'
  properties: {
    publicAccess: 'None'
  }
}

// PostgreSQL Flexible Server with pgvector
resource postgresql 'Microsoft.DBforPostgreSQL/flexibleServers@2023-03-01-preview' = {
  name: 'psql-${projectName}'
  location: location
  sku: {
    name: 'Standard_D2s_v3'
    tier: 'GeneralPurpose'
  }
  properties: {
    version: '16'
    administratorLogin: 'ragadmin'
    administratorLoginPassword: dbPassword
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
  }
}

// Enable pgvector extension
resource pgvectorExtension 'Microsoft.DBforPostgreSQL/flexibleServers/configurations@2023-03-01-preview' = {
  parent: postgresql
  name: 'azure.extensions'
  properties: {
    value: 'vector'
    source: 'user-override'
  }
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: 'asp-${projectName}'
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// App Service
resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: 'app-${projectName}'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      appSettings: [
        {
          name: 'AZURE_OPENAI_ENDPOINT'
          value: openai.properties.endpoint
        }
        {
          name: 'AZURE_OPENAI_DEPLOYMENT'
          value: 'gpt-4'
        }
        {
          name: 'AZURE_OPENAI_EMBEDDING_DEPLOYMENT'
          value: 'text-embedding-ada-002'
        }
        {
          name: 'AZURE_SEARCH_ENDPOINT'
          value: 'https://${search.name}.search.windows.net'
        }
        {
          name: 'AZURE_STORAGE_ACCOUNT'
          value: storage.name
        }
        {
          name: 'POSTGRESQL_HOST'
          value: postgresql.properties.fullyQualifiedDomainName
        }
        {
          name: 'POSTGRESQL_DATABASE'
          value: 'ragdb'
        }
      ]
    }
    httpsOnly: true
  }
}

// Key Vault for secrets
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-${projectName}'
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: appService.identity.principalId
        permissions: {
          secrets: ['get', 'list']
        }
      }
    ]
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
  }
}

// Outputs
output openaiEndpoint string = openai.properties.endpoint
output searchEndpoint string = 'https://${search.name}.search.windows.net'
output storageAccountName string = storage.name
output appServiceUrl string = 'https://${appService.properties.defaultHostName}'
output postgresqlHost string = postgresql.properties.fullyQualifiedDomainName
