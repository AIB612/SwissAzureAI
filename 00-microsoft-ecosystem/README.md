# 🏢 Microsoft 数字化转型完整方案

> 云基础设施 + 自动化运维 + 协作通信 + AI 的完整能力矩阵

---

## 🎯 能力矩阵总览

| 能力领域 | 工具 | 状态 |
|----------|------|------|
| ☁️ 云基础设施 | Azure, M365 | ✅ |
| ⚙️ 自动化编排 | PowerShell, Bash, Ansible, CI/CD | ✅ |
| 💬 协作通信 | Teams, SharePoint, VoIP | ✅ |
| 🤖 AI 处理 | Azure OpenAI, Semantic Kernel | ✅ |
| 📊 数据分析 | Power BI, Fabric | ✅ |

---

## ☁️ 1. 云基础设施 (Azure + M365)

### Azure 基础设施即代码 (IaC)

| 工具 | 用途 | 开源资源 |
|------|------|----------|
| **Bicep** | Azure 原生 IaC | https://github.com/Azure/bicep |
| **Terraform** | 多云 IaC | https://github.com/hashicorp/terraform-provider-azurerm |
| **Azure CLI** | 命令行管理 | https://github.com/Azure/azure-cli |
| **ALZ (Landing Zone)** | 企业级架构 | https://github.com/Azure/ALZ-Bicep |

**Bicep 部署示例:**
```bicep
// main.bicep - 部署 Web App + SQL
param location string = 'switzerlandnorth'

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'asp-prod'
  location: location
  sku: { name: 'B1' }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'app-prod-001'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
  }
}
```

```bash
# 部署
az deployment group create -g rg-prod --template-file main.bicep
```

### Azure 监控与安全

| 工具 | 用途 | 开源资源 |
|------|------|----------|
| **Azure Monitor** | 监控告警 | https://github.com/Azure/azure-monitor-baseline-alerts |
| **Log Analytics** | 日志分析 | KQL 查询语言 |
| **Microsoft Sentinel** | SIEM 安全 | https://github.com/Azure/Azure-Sentinel |
| **Defender for Cloud** | 云安全态势 | 内置 |

**监控告警 Bicep:**
```bicep
resource alert 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'cpu-alert'
  location: 'global'
  properties: {
    severity: 2
    enabled: true
    scopes: [webApp.id]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'
      allOf: [{
        name: 'HighCPU'
        metricName: 'CpuPercentage'
        operator: 'GreaterThan'
        threshold: 80
        timeAggregation: 'Average'
      }]
    }
    actions: [{ actionGroupId: actionGroup.id }]
  }
}
```

### M365 管理

| 工具 | 用途 | 开源资源 |
|------|------|----------|
| **Microsoft 365 Admin** | 租户管理 | Portal |
| **Entra ID (Azure AD)** | 身份管理 | https://github.com/AzureAD/microsoft-authentication-library-for-js |
| **Intune** | 设备管理 | https://github.com/microsoftgraph/powershell-intune-samples |
| **Exchange Online** | 邮件管理 | PowerShell |

**M365 用户批量创建:**
```powershell
# 从 CSV 批量创建用户
Import-Csv users.csv | ForEach-Object {
    New-MgUser -DisplayName $_.Name `
               -UserPrincipalName $_.UPN `
               -MailNickname $_.Alias `
               -AccountEnabled $true `
               -PasswordProfile @{
                   Password = $_.Password
                   ForceChangePasswordNextSignIn = $true
               }
}
```

---

## ⚙️ 2. 自动化与编排

### PowerShell 自动化

| 模块 | 用途 | 开源资源 |
|------|------|----------|
| **Az Module** | Azure 管理 | https://github.com/Azure/azure-powershell |
| **PnP.PowerShell** | M365/SharePoint | https://github.com/pnp/powershell |
| **Microsoft.Graph** | Graph API | https://github.com/microsoftgraph/msgraph-sdk-powershell |
| **ExchangeOnline** | 邮件管理 | 内置 |

**Azure 资源批量管理:**
```powershell
# 安装模块
Install-Module Az -Scope CurrentUser

# 登录
Connect-AzAccount

# 批量停止非生产 VM (节省成本)
Get-AzVM -ResourceGroupName "rg-dev" | 
    Where-Object { $_.Tags["Environment"] -eq "Dev" } |
    Stop-AzVM -Force

# 导出所有资源清单
Get-AzResource | 
    Select-Object Name, ResourceType, Location, ResourceGroupName |
    Export-Csv -Path "azure-inventory.csv"
```

### Bash 脚本

```bash
#!/bin/bash
# azure-deploy.sh - Azure 资源部署脚本

set -e

RESOURCE_GROUP="rg-prod"
LOCATION="switzerlandnorth"

# 登录 (CI/CD 中使用 Service Principal)
az login --service-principal -u $ARM_CLIENT_ID -p $ARM_CLIENT_SECRET --tenant $ARM_TENANT_ID

# 创建资源组
az group create --name $RESOURCE_GROUP --location $LOCATION

# 部署 Bicep
az deployment group create \
    --resource-group $RESOURCE_GROUP \
    --template-file main.bicep \
    --parameters @params.json

# 验证部署
az webapp show --name app-prod-001 --resource-group $RESOURCE_GROUP --query state

echo "✅ Deployment completed"
```

### Ansible AWX

| 资源 | 链接 |
|------|------|
| **AWX (开源 Tower)** | https://github.com/ansible/awx |
| **Azure Collection** | https://github.com/ansible-collections/azure |
| **Windows Collection** | https://github.com/ansible-collections/ansible.windows |

**Ansible Playbook - Azure VM:**
```yaml
# deploy-vm.yml
---
- name: Deploy Azure VM
  hosts: localhost
  connection: local
  collections:
    - azure.azcollection

  tasks:
    - name: Create resource group
      azure_rm_resourcegroup:
        name: rg-ansible
        location: switzerlandnorth

    - name: Create virtual network
      azure_rm_virtualnetwork:
        resource_group: rg-ansible
        name: vnet-prod
        address_prefixes: "10.0.0.0/16"

    - name: Create VM
      azure_rm_virtualmachine:
        resource_group: rg-ansible
        name: vm-web-01
        vm_size: Standard_B2s
        admin_username: azureuser
        ssh_password_enabled: false
        ssh_public_keys:
          - path: /home/azureuser/.ssh/authorized_keys
            key_data: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
        image:
          offer: 0001-com-ubuntu-server-jammy
          publisher: Canonical
          sku: 22_04-lts
          version: latest
```

**AWX 安装 (Docker):**
```bash
git clone https://github.com/ansible/awx.git
cd awx
make docker-compose-build
docker-compose up -d
# 访问: http://localhost:8052
```

### CI/CD 流水线

#### GitHub Actions

```yaml
# .github/workflows/azure-deploy.yml
name: Azure Deployment

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
          resourceGroupName: rg-prod
          template: ./infra/main.bicep
          
      - name: Run Ansible
        run: |
          pip install ansible azure-cli
          ansible-playbook deploy.yml
```

#### Azure DevOps Pipeline

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: Build
    jobs:
      - job: Validate
        steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'Azure-Connection'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                az bicep build --file main.bicep

  - stage: Deploy
    jobs:
      - deployment: Production
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureResourceManagerTemplateDeployment@3
                  inputs:
                    deploymentScope: 'Resource Group'
                    azureResourceManagerConnection: 'Azure-Connection'
                    resourceGroupName: 'rg-prod'
                    location: 'Switzerland North'
                    templateLocation: 'Linked artifact'
                    csmFile: '$(Pipeline.Workspace)/main.bicep'
```

#### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        AZURE_CREDENTIALS = credentials('azure-service-principal')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-org/infra.git'
            }
        }
        
        stage('Validate') {
            steps {
                sh 'az bicep build --file main.bicep'
            }
        }
        
        stage('Deploy') {
            steps {
                withCredentials([azureServicePrincipal('azure-service-principal')]) {
                    sh '''
                        az login --service-principal \
                            -u $AZURE_CLIENT_ID \
                            -p $AZURE_CLIENT_SECRET \
                            --tenant $AZURE_TENANT_ID
                        
                        az deployment group create \
                            --resource-group rg-prod \
                            --template-file main.bicep
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                sh 'ansible-playbook test-deployment.yml'
            }
        }
    }
    
    post {
        success {
            slackSend channel: '#deployments', message: "✅ Deployment successful"
        }
        failure {
            slackSend channel: '#deployments', message: "❌ Deployment failed"
        }
    }
}
```

---

## 💬 3. 协作通信 (Teams, SharePoint, VoIP)

### Microsoft Teams

| 功能 | 工具 | 开源资源 |
|------|------|----------|
| **Teams 管理** | PowerShell | https://github.com/MicrosoftDocs/office-docs-powershell |
| **Teams Apps** | Teams Toolkit | https://github.com/OfficeDev/Microsoft-Teams-Samples |
| **Teams Bot** | Bot Framework | https://github.com/microsoft/botframework-sdk |
| **Webhooks** | Incoming Webhook | 内置 |

**Teams 自动化管理:**
```powershell
# 安装 Teams 模块
Install-Module MicrosoftTeams

# 连接
Connect-MicrosoftTeams

# 批量创建团队
$teams = @(
    @{Name="项目A"; Description="项目A团队"; Visibility="Private"},
    @{Name="项目B"; Description="项目B团队"; Visibility="Private"}
)

$teams | ForEach-Object {
    New-Team -DisplayName $_.Name -Description $_.Description -Visibility $_.Visibility
}

# 添加频道
New-TeamChannel -GroupId $teamId -DisplayName "开发" -Description "开发讨论"
New-TeamChannel -GroupId $teamId -DisplayName "测试" -Description "测试反馈"
```

**Teams Webhook 通知:**
```bash
#!/bin/bash
# 发送部署通知到 Teams

WEBHOOK_URL="https://outlook.office.com/webhook/xxx"

curl -H "Content-Type: application/json" -d '{
    "@type": "MessageCard",
    "themeColor": "0076D7",
    "summary": "部署通知",
    "sections": [{
        "activityTitle": "✅ 生产环境部署成功",
        "facts": [
            {"name": "环境", "value": "Production"},
            {"name": "版本", "value": "v1.2.3"},
            {"name": "时间", "value": "'$(date)'"}
        ]
    }]
}' $WEBHOOK_URL
```

### SharePoint

| 功能 | 工具 | 开源资源 |
|------|------|----------|
| **站点管理** | PnP PowerShell | https://github.com/pnp/powershell |
| **SPFx 开发** | SharePoint Framework | https://github.com/pnp/sp-dev-fx-webparts |
| **迁移工具** | SharePoint Migration | https://github.com/pnp/PnP-Tools |

**SharePoint 站点批量创建:**
```powershell
# 批量创建项目站点
$sites = @(
    @{Url="sites/ProjectA"; Title="项目A"; Template="STS#3"},
    @{Url="sites/ProjectB"; Title="项目B"; Template="STS#3"}
)

$sites | ForEach-Object {
    New-PnPSite -Type TeamSite `
        -Title $_.Title `
        -Alias ($_.Url -replace "sites/","") `
        -Description "项目协作站点"
}
```

### VoIP / Teams Phone

| 功能 | 工具 | 说明 |
|------|------|------|
| **Teams Phone** | Teams Admin | 企业电话系统 |
| **Direct Routing** | SBC | 连接 PSTN |
| **Auto Attendant** | Teams Admin | 自动话务员 |
| **Call Queue** | Teams Admin | 呼叫队列 |

**Teams Phone 配置 (PowerShell):**
```powershell
# 分配电话号码
Set-CsPhoneNumberAssignment -Identity user@contoso.com `
    -PhoneNumber "+41441234567" `
    -PhoneNumberType DirectRouting

# 创建呼叫队列
New-CsCallQueue -Name "客服热线" `
    -LanguageId "zh-CN" `
    -UseDefaultMusicOnHold $true `
    -RoutingMethod Attendant `
    -Users @("agent1@contoso.com", "agent2@contoso.com")

# 创建自动话务员
New-CsAutoAttendant -Name "总机" `
    -LanguageId "zh-CN" `
    -TimeZoneId "W. Europe Standard Time" `
    -DefaultCallFlow $defaultCallFlow
```

**SIP Trunk 配置 (Direct Routing):**
```powershell
# 添加 SBC
New-CsOnlinePSTNGateway -Identity "sbc.contoso.com" `
    -SipSignalingPort 5067 `
    -Enabled $true

# 创建语音路由
New-CsOnlineVoiceRoute -Identity "Swiss-Route" `
    -NumberPattern "^\+41(\d{9})$" `
    -OnlinePstnGatewayList "sbc.contoso.com" `
    -Priority 1
```

---

## 🔄 4. 完整自动化闭环

### 场景: 新员工入职自动化

```
HR 提交入职表单 (Power Apps)
         ↓
Power Automate 触发
         ↓
┌────────┴────────┐
│                 │
▼                 ▼
Entra ID          M365
创建用户          分配许可证
         │
         ▼
    PowerShell 脚本
    ├─ 创建邮箱
    ├─ 加入 Teams 团队
    ├─ 分配 SharePoint 权限
    └─ 配置 Teams Phone
         │
         ▼
    Ansible Playbook
    ├─ 配置 VPN 账号
    └─ 创建 AD 账号 (混合环境)
         │
         ▼
    通知 (Teams + Email)
    └─ 发送欢迎邮件 + 入职指南
```

**完整 PowerShell 脚本:**
```powershell
# onboard-user.ps1
param(
    [string]$DisplayName,
    [string]$Email,
    [string]$Department,
    [string]$PhoneNumber
)

# 1. 创建 Entra ID 用户
$password = [System.Web.Security.Membership]::GeneratePassword(16, 4)
$user = New-MgUser -DisplayName $DisplayName `
    -UserPrincipalName $Email `
    -MailNickname ($Email -split "@")[0] `
    -Department $Department `
    -AccountEnabled $true `
    -PasswordProfile @{
        Password = $password
        ForceChangePasswordNextSignIn = $true
    }

# 2. 分配 M365 许可证
Set-MgUserLicense -UserId $user.Id -AddLicenses @{SkuId = "M365_E3_SKU_ID"} -RemoveLicenses @()

# 3. 添加到 Teams 团队
Add-TeamUser -GroupId $departmentTeamId -User $Email -Role Member

# 4. 分配 Teams Phone
Set-CsPhoneNumberAssignment -Identity $Email -PhoneNumber $PhoneNumber -PhoneNumberType DirectRouting

# 5. 发送欢迎邮件
$mailParams = @{
    Message = @{
        Subject = "欢迎加入公司"
        Body = @{
            ContentType = "HTML"
            Content = "<h1>欢迎 $DisplayName!</h1><p>您的临时密码: $password</p>"
        }
        ToRecipients = @(@{EmailAddress = @{Address = $Email}})
    }
}
Send-MgUserMail -UserId "hr@contoso.com" -BodyParameter $mailParams

# 6. Teams 通知
$webhook = "https://outlook.office.com/webhook/xxx"
Invoke-RestMethod -Uri $webhook -Method Post -Body (@{
    text = "✅ 新员工 $DisplayName 入职完成"
} | ConvertTo-Json) -ContentType "application/json"

Write-Host "✅ 用户 $DisplayName 创建完成"
```

---

## 📊 能力对照表

| 要求 | 工具 | 本项目覆盖 |
|------|------|-----------|
| M365 搭建运维 | Entra ID, Exchange, Intune | ✅ |
| Azure 云基础设施 | Bicep, Terraform, ARM | ✅ |
| PowerShell 自动化 | Az, PnP, Graph, Teams | ✅ |
| Bash 脚本 | Azure CLI, Shell | ✅ |
| Jenkins CI/CD | Jenkinsfile, Pipeline | ✅ |
| Ansible AWX | Playbooks, Azure Collection | ✅ |
| CI/CD 流水线 | GitHub Actions, Azure DevOps | ✅ |
| Teams 协作 | 管理, Bot, Webhook | ✅ |
| SharePoint | PnP, SPFx | ✅ |
| VoIP 电话 | Teams Phone, Direct Routing | ✅ |

---

## 🔗 资源汇总

| 类别 | 链接 |
|------|------|
| **Azure IaC** | |
| Bicep | https://github.com/Azure/bicep |
| ALZ Landing Zone | https://github.com/Azure/ALZ-Bicep |
| Terraform Azure | https://github.com/hashicorp/terraform-provider-azurerm |
| **自动化** | |
| Az PowerShell | https://github.com/Azure/azure-powershell |
| PnP PowerShell | https://github.com/pnp/powershell |
| Ansible AWX | https://github.com/ansible/awx |
| Ansible Azure | https://github.com/ansible-collections/azure |
| **M365** | |
| Graph SDK | https://github.com/microsoftgraph/msgraph-sdk-powershell |
| Teams Samples | https://github.com/OfficeDev/Microsoft-Teams-Samples |
| SPFx Samples | https://github.com/pnp/sp-dev-fx-webparts |
| **监控安全** | |
| Azure Sentinel | https://github.com/Azure/Azure-Sentinel |
| Monitor Alerts | https://github.com/Azure/azure-monitor-baseline-alerts |
