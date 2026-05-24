# NimbusKart Cost Janitor

This project simulates a cloud cost hygiene workflow using Terraform, LocalStack, Python, and GitHub Actions.

This project simulates a FinOps/DevOps workflow where infrastructure is provisioned locally and scanned for wasteful cloud resources such as unattached EBS volumes, stopped EC2 instances, unused Elastic IPs, and improperly tagged resources.

---

# Architecture Overview

```text
GitHub Actions
       ↓
 LocalStack (AWS Emulator)
       ↓
 Terraform Infrastructure
       ↓
 Python Cost Janitor
       ↓
 JSON + Markdown Reports
```

---

# Features

## Infrastructure Provisioning
- VPC
- Public Subnets
- Security Groups
- EC2 Instances
- S3 Bucket
- Orphaned EBS Volume
- Unused Elastic IP
- Modular Terraform structure

## Cost Janitor Detection
- Unattached EBS volumes
- Stopped EC2 instances
- Unused Elastic IPs
- Missing required tags

## Reporting
- JSON report generation
- Markdown summary generation

## Safety Features
- Dry-run mode by default
- Optional delete mode
- Protected=true resource protection

## CI/CD
- GitHub Actions workflow
- Automated Terraform provisioning
- Automated Janitor execution
- Artifact uploads

---

# Repository Structure

```text
nimbuskart-cost-janitor/
│
├── terraform/
├── janitor/
├── .github/workflows/
├── docs/
├── samples/
├── README.md
├── DESIGN.md
└── SUBMISSION.md
```

---

# Prerequisites

- Docker Desktop
- Terraform >= 1.5
- Python 3.10+
- Git

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/suvan-agrawal/nimbuskart-cost-janitor.git
cd nimbuskart-cost-janitor
```

---

# Start LocalStack

```bash
docker run --rm -d -p 4566:4566 --name localstack localstack/localstack:3
```

---

# Provision Infrastructure

```bash
cd terraform

terraform init

terraform apply -auto-approve
```

---

# Run Cost Janitor

From repository root:

```bash
python janitor/janitor.py
```

---

# Run Delete Mode

```bash
python janitor/janitor.py --delete
```

---

# Run Stopped Instance Detection Demo

```bash
python janitor/janitor.py --max-stopped-days 0
```

---

# Sample Reports

Example outputs are available in:

```text
samples/
```

---

# GitHub Actions

The workflow automatically:
1. Starts LocalStack
2. Applies Terraform infrastructure
3. Executes Cost Janitor
4. Uploads reports as artifacts

Workflow file:

```text
.github/workflows/cost-janitor.yml
```

---

# Design Decisions & Deviations

## LocalStack Version Pinning

The project uses:

```text
localstack/localstack:3
```

instead of latest due to authentication/licensing behavior observed in newer releases.

---

## Terraform Local Wrapper

Standard Terraform with explicit LocalStack endpoints was preferred over terraform-local for improved portability and fewer Windows shell compatibility issues.

---

## S3 Lifecycle Configuration

S3 lifecycle configuration was excluded from active LocalStack execution due to inconsistent lifecycle API emulation causing Terraform timeouts.

The validated configuration has been retained in comments for compatibility with real AWS environments.

---

## Security Tradeoff

SSH ingress is configurable through:

```text
ssh_allowed_cidr
```

Default value:

```text
0.0.0.0/0
```

This is intentionally highlighted as insecure for production environments.

---



# AI Usage Disclosure

AI assistance was used for:
- brainstorming architecture approaches
- improving documentation clarity
- validating Terraform/Python implementation ideas

All code, debugging, integration, and final decisions were manually reviewed and tested.

---

# Author

Suvan Agrawal