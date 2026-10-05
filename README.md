# Secure AI Log Investigator

A local-first DevOps and AI incident investigation pipeline that sanitizes production-style logs, verifies that sensitive data has been removed, extracts incident patterns, estimates token usage, and uses a local Ollama/Mistral model to generate an evidence-based investigation report.

## Overview

During production incidents, engineers may use AI to investigate large volumes of logs. Raw logs can contain sensitive information such as:

- Email addresses
- IP addresses
- Authentication tokens
- Passwords
- Authorization headers
- Internal hostnames
- Request IDs
- Customer identifiers

This project demonstrates a safer approach where logs are sanitized and security-checked before they are provided to the AI investigation stage.

## Architecture

```text
Synthetic Logs
      |
      v
Sanitization
      |
      v
Security Gate
   PASS | FAIL
      |      |
      |      +----> AI Investigation Blocked
      |
      v
Pattern Extraction
      |
      v
Token Estimation
      |
      v
Local Ollama / Mistral
      |
      v
Investigation Report
      |
      v
Human Validation
Key Features
Sensitive-data sanitization

The sanitizer detects and replaces sensitive values including:

Email addresses
IP addresses
Tokens
JWTs
Authorization headers
Passwords
AWS access keys
Private keys
Request IDs
Internal hostnames
Phone numbers

Example:

Before:
user=john@example.com ip=10.10.12.5 token=api-token-demo

After:
user=[EMAIL] ip=[IP] token=[TOKEN]
Fail-closed security gate

A second security scanning layer checks the sanitized log and incident summary.

If sensitive patterns remain:

Security Gate: FAIL
AI investigation: BLOCKED

If the data passes:

Security Gate: PASS
AI investigation: ALLOWED

This provides defense in depth instead of relying only on the sanitizer.

Incident pattern extraction

The pipeline extracts useful incident information such as:

Critical events
Errors
Warnings
Important event counts
Normalized log patterns

This reduces unnecessary log noise before AI analysis.

Token estimation

The project compares approximate token usage before and after log processing to demonstrate how preprocessing can reduce the amount of data sent to an AI model.

Local AI investigation

The final investigation runs locally using:

Ollama
Mistral

No production logs need to be sent to an external AI service for this demonstration.

Project Structure
.
├── ai_investigator.py
├── generate_logs.py
├── pattern_extractor.py
├── sanitizer.py
├── security_scanner.py
├── token_estimator.py
├── run_demo.sh
├── requirements.txt
├── requirements-dev.txt
├── tests/
│   ├── test_pattern_extractor.py
│   ├── test_sanitizer.py
│   ├── test_security_scanner.py
│   └── test_token_estimator.py
└── .github/
    └── workflows/
        └── ci.yml
Requirements
Python 3.10+
Ollama
Mistral

Install the development dependencies:

pip install -r requirements-dev.txt

Install Ollama separately and pull the model:

ollama pull mistral

Verify:

ollama list
Run the Demo

Run the complete pipeline:

bash run_demo.sh

Or run each stage individually:

python generate_logs.py
python sanitizer.py
python pattern_extractor.py
python token_estimator.py
python ai_investigator.py
Testing

Run the automated tests:

pytest -v

Run linting:

ruff check .

The project also uses GitHub Actions to automatically run:

Pytest
Ruff
Gitleaks secret scanning
Security Model

The project uses multiple defensive layers:

Sensitive data is sanitized.
Sanitized output is scanned again.
The AI stage is blocked if the security gate fails.
AI analysis is performed locally using Ollama.
The generated investigation is treated as advisory and requires human validation.
Limitations

This is a demonstration project using synthetic logs.

The security scanner uses pattern matching and should not be considered a complete DLP solution. Token estimation is approximate, and AI-generated root-cause analysis should always be validated against the underlying evidence.

Future Improvements
Add structured JSON log ingestion
Expand secret and PII detection
Add configurable security policies
Add incident severity scoring
Add dashboard-based investigation
Add support for additional local LLMs