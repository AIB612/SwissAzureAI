# ⚙️ Automation & Infrastructure as Code

> Terraform, Bicep, CI/CD

---

## 📁 Files

| File | Description |
|------|-------------|
| `terraform/main.tf` | Full Azure infrastructure |
| `github-actions/deploy.yml` | CI/CD workflow |

---

## 🚀 Deploy with Terraform

```bash
cd terraform
terraform init
terraform plan -var="db_password=YourPassword"
terraform apply
```

---

## 🔄 CI/CD with GitHub Actions

Copy `github-actions/deploy.yml` to `.github/workflows/deploy.yml`

Required secrets:
- `AZURE_CREDENTIALS`
- `ARM_CLIENT_ID`
- `ARM_CLIENT_SECRET`
- `ARM_SUBSCRIPTION_ID`
- `ARM_TENANT_ID`
- `DB_PASSWORD`

---

## 📚 Microsoft Resources

- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/)
- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [GitHub Actions for Azure](https://github.com/Azure/actions)
