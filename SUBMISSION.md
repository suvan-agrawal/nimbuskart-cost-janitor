# Submission Summary

## Candidate
Suvan Agrawal

---
# Repository

GitHub Repository:

```text
https://github.com/suvan-agrawal/nimbuskart-cost-janitor
```

# Project

NimbusKart Cost Janitor

A local-first cloud cost hygiene and orphan resource detection system built using:
- Terraform
- LocalStack
- Python
- GitHub Actions

---

# Implemented Features

## Terraform Infrastructure
- VPC
- Public subnets
- Security group
- EC2 instances
- S3 bucket
- orphaned EBS volume
- unused Elastic IP

---

## Cost Janitor Detection
- Unattached EBS volumes
- Stopped EC2 instances
- Unused Elastic IPs
- Missing required tags

---

## Safety Features
- Dry-run mode by default
- Optional delete mode
- Protected=true resource protection

---

# Reports
The scanner generates:
- JSON reports
- Markdown summaries

Example reports are available in:

```text
samples/
```

---

# CI/CD

GitHub Actions workflow automates:
- LocalStack startup
- Terraform provisioning
- Janitor execution
- artifact uploads

Workflow file:

```text
.github/workflows/cost-janitor.yml
```

---

# Documentation

| File | Purpose |
|---|---|
| README.md | Setup and usage guide |
| DESIGN.md | Architecture and design decisions |
| docs/walkthrough.md | Walkthrough talking points |

---

# Notes

## LocalStack Compatibility

S3 lifecycle configuration was excluded from active LocalStack execution because lifecycle APIs caused timeout issues during local emulation.

The validated Terraform configuration has been retained in comments.

---

## Terraform Runtime Artifacts

Terraform state files and provider binaries were excluded from version control using `.gitignore` for repository hygiene and reproducibility.

---

