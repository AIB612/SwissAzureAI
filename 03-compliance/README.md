# 📋 Swiss Compliance Framework

> FADP, GDPR, SOC2, FINMA for AI Systems

---

## 🇨🇭 FADP - Federal Act on Data Protection

**Effective:** September 1, 2023

### Key Requirements

| Article | Requirement | AI Implementation |
|---------|-------------|-------------------|
| Art. 6 | Data processing principles | Document all AI data flows |
| Art. 7 | Privacy by design | Build privacy into architecture |
| Art. 8 | Data security | Encryption, access controls |
| Art. 19 | Information obligation | Explain AI decisions |
| Art. 21 | Automated decisions | Human review for significant decisions |
| Art. 25 | Right of access | API for data subject requests |
| Art. 32 | Right to erasure | Data deletion capabilities |

### FADP Checklist for AI Systems

```
□ Data inventory documented
□ Legal basis for processing identified
□ Privacy impact assessment completed
□ Data retention policy defined
□ Cross-border transfer assessment (if applicable)
□ Security measures implemented
□ Data subject rights APIs available
□ Incident response plan ready
```

---

## 🇪🇺 GDPR Alignment

Switzerland is not in the EU but maintains GDPR adequacy.

| GDPR | FADP | Notes |
|------|------|-------|
| Art. 5 - Principles | Art. 6 | Similar principles |
| Art. 6 - Lawfulness | Art. 6 | Legal basis required |
| Art. 13-14 - Information | Art. 19 | Transparency |
| Art. 17 - Erasure | Art. 32 | Right to be forgotten |
| Art. 22 - Automated decisions | Art. 21 | Human oversight |
| Art. 25 - Privacy by design | Art. 7 | Built-in privacy |
| Art. 32 - Security | Art. 8 | Technical measures |

---

## 🏦 FINMA Requirements

For financial services AI applications:

### FINMA Circular 2023/1 - Operational Risks

| Requirement | Implementation |
|-------------|----------------|
| Model Risk Management | Document AI model lifecycle |
| Outsourcing | Cloud provider due diligence |
| Business Continuity | Disaster recovery for AI systems |
| Cyber Security | Penetration testing, monitoring |

### Banking Secrecy (Art. 47 Banking Act)

```
⚠️ CRITICAL: Customer data must NEVER leave Switzerland
   for banking applications
```

---

## 🔐 SOC2 Type II

### Trust Service Criteria

| Category | AI Considerations |
|----------|-------------------|
| Security | Access controls, encryption, logging |
| Availability | SLA, redundancy, failover |
| Processing Integrity | Model accuracy, bias testing |
| Confidentiality | Data classification, DLP |
| Privacy | FADP/GDPR alignment |

### Evidence Collection

```yaml
# Required documentation
security:
  - access_control_matrix.xlsx
  - encryption_standards.md
  - penetration_test_report.pdf
  - incident_response_plan.md

availability:
  - sla_definition.md
  - disaster_recovery_plan.md
  - uptime_reports/

processing_integrity:
  - model_validation_report.pdf
  - bias_assessment.md
  - accuracy_metrics.json

confidentiality:
  - data_classification_policy.md
  - dlp_configuration.md

privacy:
  - privacy_impact_assessment.pdf
  - data_subject_request_log.xlsx
```

---

## 📍 Data Residency

### Switzerland-Only Deployment

```
┌─────────────────────────────────────────┐
│         Switzerland Border              │
│  ┌───────────────────────────────────┐  │
│  │                                   │  │
│  │  ✅ Azure Switzerland North       │  │
│  │  ✅ Swisscom Cloud                │  │
│  │  ✅ On-premises Swiss DC          │  │
│  │                                   │  │
│  │  ❌ No data transfer outside      │  │
│  │                                   │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Azure Data Residency Configuration

```bicep
// Enforce Switzerland North only
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: 'switzerlandnorth'
  properties: {
    // Disable geo-redundant storage
    // to prevent data leaving Switzerland
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
  sku: {
    name: 'Standard_LRS'  // Local redundancy only
  }
}
```

---

## 📝 Templates

### Privacy Impact Assessment (PIA)

```markdown
# Privacy Impact Assessment

## 1. Project Overview
- Name: [AI System Name]
- Purpose: [Business purpose]
- Data processed: [Categories]

## 2. Data Flow
[Diagram of data flow]

## 3. Legal Basis
- [ ] Consent
- [ ] Contract
- [ ] Legal obligation
- [ ] Legitimate interest

## 4. Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | ... | ... | ... |

## 5. Conclusion
[Recommendation]
```

### Data Processing Agreement (DPA) Checklist

```
□ Processor obligations defined
□ Sub-processor approval process
□ Data breach notification (72h)
□ Audit rights included
□ Data deletion upon termination
□ Cross-border transfer restrictions
□ Technical measures specified
```

---

## 🔗 Official Resources

| Resource | Link |
|----------|------|
| FADP Full Text | [fedlex.admin.ch](https://www.fedlex.admin.ch/eli/cc/2022/491) |
| FDPIC (Commissioner) | [edoeb.admin.ch](https://www.edoeb.admin.ch) |
| FINMA Circulars | [finma.ch](https://www.finma.ch/en/documentation/circulars/) |
| SOC2 Framework | [aicpa.org](https://www.aicpa.org/soc2) |

---

## ⚠️ Disclaimer

This documentation is for informational purposes only and does not constitute legal advice. Consult with qualified legal counsel for compliance matters.
