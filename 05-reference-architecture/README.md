# 🏛️ Reference Architecture

> Enterprise AI Architecture Patterns for Swiss Compliance

---

## 🎯 Architecture Decision Matrix

| Requirement | Azure Native | Private (pgvector) | Hybrid |
|-------------|--------------|-------------------|--------|
| Data Residency | ✅ Switzerland North | ✅ On-premises | ✅ Both |
| FADP Compliance | ✅ | ✅ | ✅ |
| FINMA Banking | ⚠️ Review needed | ✅ Full control | ✅ |
| Cost | 💰💰💰 | 💰💰 | 💰💰💰 |
| Scalability | ✅ Auto-scale | ⚠️ Manual | ✅ |
| Maintenance | ✅ Managed | ⚠️ Self-managed | ⚠️ |

---

## 🏗️ Architecture Patterns

### Pattern 1: Azure Native RAG

Best for: General enterprise, non-banking

```
┌─────────────────────────────────────────────────────────────────┐
│                    Azure Switzerland North                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Virtual Network                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │ App Service │  │ Azure OpenAI│  │ AI Search   │      │   │
│  │  │ (Frontend)  │  │ (Private EP)│  │ (Private EP)│      │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │   │
│  │         │                │                │              │   │
│  │         └────────────────┼────────────────┘              │   │
│  │                          │                               │   │
│  │  ┌─────────────┐  ┌──────┴──────┐  ┌─────────────┐      │   │
│  │  │ Key Vault   │  │ PostgreSQL  │  │ Blob Storage│      │   │
│  │  │ (Secrets)   │  │ (pgvector)  │  │ (Documents) │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Monitoring                             │   │
│  │  Log Analytics  │  Application Insights  │  Alerts       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern 2: Private Deployment

Best for: Banking, highly regulated industries

```
┌─────────────────────────────────────────────────────────────────┐
│                    Swiss Data Center                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Kubernetes Cluster                     │   │
│  │                                                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │   Nginx     │  │   FastAPI   │  │   Ollama    │      │   │
│  │  │  Ingress    │──│   (RAG)     │──│   (LLM)     │      │   │
│  │  └─────────────┘  └──────┬──────┘  └─────────────┘      │   │
│  │                          │                               │   │
│  │  ┌─────────────┐  ┌──────┴──────┐  ┌─────────────┐      │   │
│  │  │  Vault      │  │ PostgreSQL  │  │   MinIO     │      │   │
│  │  │ (Secrets)   │  │ (pgvector)  │  │ (Storage)   │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Monitoring                             │   │
│  │  Prometheus  │  Grafana  │  ELK Stack                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern 3: Hybrid (Recommended for Banking)

Best for: Banks needing Azure services but strict data control

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ┌─────────────────────────┐    ┌─────────────────────────┐    │
│  │   Azure Switzerland     │    │   On-Premises / Swiss   │    │
│  │        North            │    │      Data Center        │    │
│  │                         │    │                         │    │
│  │  ┌─────────────────┐   │    │  ┌─────────────────┐   │    │
│  │  │  Azure OpenAI   │   │    │  │  Customer Data  │   │    │
│  │  │  (No customer   │◄──┼────┼──│  (PostgreSQL    │   │    │
│  │  │   data stored)  │   │    │  │   + pgvector)   │   │    │
│  │  └─────────────────┘   │    │  └─────────────────┘   │    │
│  │                         │    │                         │    │
│  │  ┌─────────────────┐   │    │  ┌─────────────────┐   │    │
│  │  │  App Service    │   │    │  │  Document       │   │    │
│  │  │  (Stateless)    │◄──┼────┼──│  Storage        │   │    │
│  │  └─────────────────┘   │    │  └─────────────────┘   │    │
│  │                         │    │                         │    │
│  └─────────────────────────┘    └─────────────────────────┘    │
│                                                                  │
│              ExpressRoute / VPN (Encrypted)                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: Network Security                                        │
│ - Private Endpoints (no public internet)                         │
│ - Network Security Groups                                        │
│ - Azure Firewall / WAF                                          │
├─────────────────────────────────────────────────────────────────┤
│ Layer 2: Identity & Access                                       │
│ - Microsoft Entra ID (Azure AD)                                 │
│ - Managed Identities                                            │
│ - RBAC (Role-Based Access Control)                              │
├─────────────────────────────────────────────────────────────────┤
│ Layer 3: Data Protection                                         │
│ - Encryption at rest (AES-256)                                  │
│ - Encryption in transit (TLS 1.3)                               │
│ - Customer-managed keys (Key Vault)                             │
├─────────────────────────────────────────────────────────────────┤
│ Layer 4: Application Security                                    │
│ - Input validation                                              │
│ - Output sanitization                                           │
│ - Rate limiting                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Layer 5: Monitoring & Audit                                      │
│ - Azure Monitor / Log Analytics                                 │
│ - Security Center / Defender                                    │
│ - Audit logs (90+ days retention)                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Cost Estimation (Monthly)

### Azure Native (Small)

| Service | SKU | Cost (CHF) |
|---------|-----|------------|
| Azure OpenAI | S0 + usage | ~500-2000 |
| AI Search | Standard | ~250 |
| PostgreSQL | GP_D2s_v3 | ~200 |
| App Service | P1v3 | ~150 |
| Storage | 100GB | ~5 |
| Key Vault | Standard | ~5 |
| **Total** | | **~1100-2600** |

### Private Deployment (Small)

| Component | Spec | Cost (CHF) |
|-----------|------|------------|
| Server (GPU) | RTX 4090 | ~300 (hosting) |
| Storage | 1TB NVMe | ~50 |
| Bandwidth | 1Gbps | ~100 |
| Backup | 500GB | ~30 |
| **Total** | | **~480** |

---

## 📋 Implementation Checklist

```
Phase 1: Foundation (Week 1-2)
□ Azure subscription setup
□ Resource group creation
□ Network architecture (VNet, subnets)
□ Key Vault deployment
□ Managed identities

Phase 2: Core Services (Week 3-4)
□ Azure OpenAI deployment
□ AI Search setup
□ PostgreSQL + pgvector
□ Storage account
□ Private endpoints

Phase 3: Application (Week 5-6)
□ RAG application deployment
□ Document ingestion pipeline
□ API development
□ Frontend deployment

Phase 4: Security & Compliance (Week 7-8)
□ Security hardening
□ FADP compliance review
□ Penetration testing
□ Documentation
□ SOC2 evidence collection

Phase 5: Operations (Ongoing)
□ Monitoring setup
□ Alerting configuration
□ Backup verification
□ Disaster recovery testing
□ Performance optimization
```

---

## 📚 References

- [Azure OpenAI Landing Zone](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/azure-openai-baseline-landing-zone)
- [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
- [Swiss Financial Market Supervisory Authority](https://www.finma.ch)
