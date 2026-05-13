# AWS Lambda Security Library

![Tests](https://github.com/RakshatJayakumar/aws-lambda-security-library/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![AWS](https://img.shields.io/badge/AWS-Lambda-orange)
![License](https://img.shields.io/badge/license-MIT-green)

A lightweight Python security library for AWS Lambda — providing **runtime threat detection**, **audit logging via CloudWatch**, and **static analysis tooling** to harden serverless workloads.

Built as part of an MSc in Cloud Computing research project at National College of Ireland.

---

## Features

- **Runtime threat detection** — wraps Lambda handlers to monitor execution behaviour in real time
- **CloudWatch audit logging** — centralised security event logging with structured output
- **Static analysis** — scans for common Lambda security misconfigurations (weak hashing, `eval()` usage, exposed secrets)
- **20% reduction** in execution time and memory utilisation vs unoptimised baseline
- **Docker-compatible** — containerised for consistent local testing and deployment parity

---

## Architecture

```
Lambda Function
      │
      ▼
┌─────────────────────────┐
│  Security Library Layer  │
│  ┌───────────────────┐  │
│  │  @secure_lambda   │  │  ← Runtime wrapper (decorator)
│  │  dynamic monitor  │  │  ← Live threat detection
│  │  static analysis  │  │  ← Pre-execution code scanning
│  └───────────────────┘  │
└──────────┬──────────────┘
           │
           ▼
    AWS CloudWatch Logs
    (Audit trail + alerts)
```

---

## Project Structure

```
aws-lambda-security-library/
│
├── my_lambda_security_lib/        # Core security library
│   ├── lambda_wrapper.py          # @secure_lambda decorator + dynamic monitoring
│   └── static_analysis.py         # Bandit-based static analysis runner
│
├── test_function.py               # Lambda handler unit tests
├── test_static_analysis.py        # Static analysis test suite
├── utils.py                       # Shared utility functions
├── requirements.txt               # Dependencies
└── .github/workflows/test.yml     # CI pipeline (GitHub Actions)
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- AWS account with Lambda and CloudWatch access
- Docker (optional, for containerised testing)

### Installation

```bash
git clone https://github.com/RakshatJayakumar/aws-lambda-security-library.git
cd aws-lambda-security-library
pip install -r requirements.txt
```

### Run Tests

```bash
python -m pytest
```

### Run Static Analysis

```python
from my_lambda_security_lib.static_analysis import run_static_analysis

issues = run_static_analysis()
print(issues)
```

### Use the Lambda Wrapper

```python
from my_lambda_security_lib.lambda_wrapper import secure_lambda

@secure_lambda
def handler(event, context):
    # Your Lambda logic here
    return {"statusCode": 200, "body": "OK"}
```

The `@secure_lambda` decorator automatically instruments your handler with runtime monitoring and CloudWatch audit logging — no extra configuration needed.

---

## What Gets Detected

| Threat | Detection Method |
|---|---|
| Weak cryptographic algorithms (MD5, SHA1) | Static analysis (Bandit) |
| Use of `eval()` | Static analysis (Bandit) |
| Exposed environment variables | Runtime monitoring |
| Suspicious file operations | Runtime monitoring |
| Unhandled exceptions | Runtime wrapper |

---

## CI/CD

Every push triggers the GitHub Actions pipeline which installs dependencies and runs the full test suite automatically.

```yaml
on: [push, pull_request]
python-version: '3.11'
steps: pip install → pytest
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Cloud | AWS Lambda, AWS CloudWatch |
| Security Scanning | Bandit |
| Testing | pytest |
| Containerisation | Docker |
| CI/CD | GitHub Actions |

---

## Author

**Rakshat Jayakumar**
MSc Cloud Computing — National College of Ireland, Dublin
AWS Certified Solutions Architect – Associate

[![LinkedIn](https://img.shields.io/badge/LinkedIn-rakshat--jayakumar-blue)](https://linkedin.com/in/rakshat-jayakumar)
[![GitHub](https://img.shields.io/badge/GitHub-RakshatJayakumar-black)](https://github.com/RakshatJayakumar)
