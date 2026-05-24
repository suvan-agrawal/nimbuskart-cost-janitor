# Design Notes

## Overview

The project was designed as a lightweight local-first cloud cost hygiene system using LocalStack, Terraform, Python, and GitHub Actions.

The primary goal was to simulate real-world cloud cost optimization workflows without requiring access to an actual AWS account.

The implementation focuses on:
- reproducibility
- modular infrastructure
- safe automation
- CI/CD integration
- clear reporting

rather than enterprise-scale complexity.

---

# Infrastructure Design

Terraform was used to provision simulated AWS infrastructure on top of LocalStack.

The infrastructure includes:
- VPC
- public subnets
- security group
- EC2 instances
- S3 bucket
- orphaned EBS volumes
- unused Elastic IP

A reusable Terraform module was created for the networking layer to improve maintainability without overengineering the project structure.

---

# Janitor Design

The Cost Janitor was implemented in Python using boto3.

The scanner currently detects:
- unattached EBS volumes
- stopped EC2 instances
- unused Elastic IPs
- resources missing required tags

The scanner generates:
- machine-readable JSON reports
- markdown summaries for humans

Delete operations are optional and disabled by default.

---

# Safety Mechanisms

Several safety controls were intentionally included:

## Dry-run by Default

The scanner reports findings without deleting resources unless the `--delete` flag is explicitly provided.

---

## Protected Resources

Resources tagged with:

```text
Protected=true
```

are skipped during automated deletion.

---

## Conservative EC2 Handling

Stopped EC2 instances are intentionally marked:

```text
safe_to_auto_delete = false
```

because deleting compute resources automatically in production environments can be risky.

---

# CI/CD Design

GitHub Actions was used to automate:
- LocalStack startup
- Terraform provisioning
- Cost Janitor execution
- report artifact uploads

The workflow was intentionally kept simple and reproducible so it can run successfully on fresh repository clones.

---

# Multi-Cloud Extension Strategy

The current implementation is AWS-oriented due to assignment scope.

Future multi-cloud support could be implemented by:
- abstracting provider-specific scanners
- introducing provider adapters
- standardizing resource finding schemas

Example structure:

```text
providers/
 ├── aws/
 ├── gcp/
 └── azure/
```

Each provider module would expose:
- scan resources
- normalize findings
- execute cleanup safely

---

# IAM Considerations

A production implementation would follow least-privilege access principles.

The scanner would require read-only permissions for:
- EC2
- EBS
- Elastic IPs
- tagging APIs

Delete mode would require explicitly separate elevated permissions.

---

# Observability Improvements

If extended further, the system could expose:
- Prometheus metrics
- CloudWatch dashboards
- cleanup audit logs
- historical trend reports

---

# Decisions & Trade-offs

## LocalStack Version Pinning

The LocalStack image was pinned to:

```text
localstack/localstack:3
```

due to authentication/licensing issues encountered with newer versions.

---

## Terraform Local Wrapper

The `terraform-local` wrapper was evaluated initially but standard Terraform with explicit LocalStack endpoints was ultimately preferred for improved portability and fewer Windows shell compatibility issues.

---

## S3 Lifecycle Configuration

S3 lifecycle configuration was excluded from active LocalStack execution because lifecycle APIs caused repeated timeout behavior during local emulation.

The validated Terraform configuration was retained in comments for compatibility with real AWS environments.

---

# What Was Intentionally Not Implemented

The following were intentionally excluded to keep the project focused and stable within assignment scope:
- Kubernetes integration
- distributed scheduling
- database persistence
- dashboard UI
- real AWS billing APIs
- aggressive automatic cleanup policies

The implementation prioritizes correctness and reproducibility over feature breadth.