# Secure AI Log Investigator

A local-first incident investigation pipeline that uses AI without sending raw production-style logs directly to an external AI service.

I built this project around a simple problem: AI can be useful during an incident, but logs can also contain credentials, personal information and internal infrastructure details.

Instead of giving the model the raw logs, the project puts a security and preprocessing layer in front of the AI.

## How It Works

```text
                    Raw / Synthetic Logs
                            |
                            v
                       Sanitization
                            |
                            v
                      Security Gate
                       /          \
                    PASS            FAIL
                     |                |
                     v                v
              Pattern Extraction   AI blocked
                     |
                     v
               Token Estimation
                     |
                     v
                Local LLM
              Ollama / Mistral
                     |
                     v
             Investigation Report
                     |
                     v
              Human Validation

The important part is the security gate.
Sanitizing a log does not automatically mean that every sensitive value has been removed. The pipeline therefore scans the processed data again before allowing it to reach the AI stage.
If the security gate finds something that should not be passed to the model, the AI investigation is stopped.
Pipeline in action
<img width="1090" height="827" alt="bash1" src="https://github.com/user-attachments/assets/f304ce8f-f6b9-4069-9146-a225f36f7371" />
<img width="1006" height="761" alt="bash 2" src="https://github.com/user-attachments/assets/33948f0e-c2ef-45f2-b846-ec6edbbcb1fb" />
<img width="888" height="807" alt="bash3" src="https://github.com/user-attachments/assets/25a8c41e-f98a-410d-b99f-a4958a518b18" />

 
What the project does
1. Sanitizes log data
The sanitizer looks for common sensitive values and replaces them with safe placeholders.
It currently handles things such as:
- Email addresses
- IP addresses
- Authentication tokens
- JWTs
- Passwords
- Authorization headers
- AWS access keys
- Private keys
- Internal hostnames
- Request IDs
- Phone numbers
For example:
Before:

user=john@example.com ip=10.10.12.5 token=api-token-demo

becomes:
After:

user=[EMAIL] ip=[IP] token=[TOKEN]

The idea is not to make the logs useless. The goal is to remove sensitive values while keeping enough context for the investigation.
2. Runs a security gate
After sanitization, the resulting data is scanned again.
Sanitized data
      |
      v
Security Scanner
      |
   +--+--+
   |     |
 PASS   FAIL
   |     |
   v     v
Continue  Stop

A failed scan blocks the AI investigation.
This gives the pipeline a fail-closed behaviour rather than assuming that the sanitizer always catches everything.
3. Extracts incident patterns
The project extracts useful information from the logs before sending anything to the model.
This includes:
- Important event counts
- Critical events
- Errors
- Warnings
- Repeated log patterns
This helps reduce unnecessary log noise and gives the AI a smaller, more useful set of evidence to work with.
4. Estimates token usage
The pipeline compares the approximate amount of text before and after processing.
This is useful for seeing how much data is being carried through the investigation pipeline.
The token calculation is intentionally an estimate rather than an exact model tokenizer count.
5. Investigates the incident locally
The final analysis is performed using a local LLM through:
- Ollama
- Mistral
The model receives the processed investigation data rather than the original raw logs.
The generated investigation covers areas such as:
- Incident summary
- Severity
- Likely root cause
- Supporting evidence
- Investigation commands
- Recommended remediation
- AI confidence
- Human validation
The AI output is treated as advisory, not as an automatic decision.
Example investigation report
<img width="1119" height="802" alt="Screenshot 2026-10-06 at 6 23 53 am" src="https://github.com/user-attachments/assets/6c6b3a4e-c3c9-4547-a7f1-09bb39e0817e" />

 
6. Tests and CI
The project includes automated tests for the main pipeline components.
Run the tests locally with:
pytest -v

Lint the project with:
ruff check .

GitHub Actions runs the validation automatically and includes:
- Pytest
- Ruff
- Gitleaks secret scanning
The local AI model is not required by CI. The workflow focuses on testing the deterministic parts of the pipeline and checking the repository for accidentally committed secrets.
GitHub Actions
<img width="1469" height="718" alt="Screenshot 2026-10-06 at 6 22 52 am" src="https://github.com/user-attachments/assets/3e27e11e-3540-4c09-a82a-aece7b3730d0" />

 
Project structure
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
├── docs/
│   └── images/
│       ├── pipeline-demo.png
│       ├── ai-investigation-report.png
│       └── github-actions.png
└── .github/
    └── workflows/
        └── ci.yml

Running it locally
Requirements
- Python 3.10+
- Ollama
- Mistral
Install the development dependencies:
pip install -r requirements-dev.txt

Install the local model:
ollama pull mistral

Then run the complete demonstration:
bash run_demo.sh

The individual stages can also be run separately:
python generate_logs.py
python sanitizer.py
python pattern_extractor.py
python token_estimator.py
python ai_investigator.py

Security approach
The project deliberately uses multiple checks rather than relying on a single sanitizer.
Raw logs
   ↓
Redaction
   ↓
Security scan
   ↓
AI input
   ↓
Local model

The main principles are:
1. Sensitive values are removed before AI processing.
2. The processed data is scanned again.
3. A failed security check blocks the AI stage.
4. The LLM runs locally through Ollama.
5. AI-generated conclusions require human validation.
6. CI scans the repository for accidentally committed secrets.
Limitations
This is a demonstration project and uses synthetic logs.
The security scanner is pattern-based, so it should not be considered a complete DLP or enterprise data-classification solution.
Similarly, the token calculation is approximate and the AI-generated root-cause analysis can be wrong. The final investigation should always be checked against the underlying evidence.
Possible next steps
Some areas I would explore next:
- Structured JSON log ingestion
- More extensive PII and secret detection
- Configurable security policies
- Incident severity scoring
- Additional local LLM support
- Prometheus and Alertmanager integration
- Automated incident correlation
- Dashboard-based investigation
Why I built this
I wanted to explore where AI can actually help with day-to-day platform and incident work without treating the model as a trusted destination for raw operational data.
The project is intentionally small enough to run locally, but the design is based around a problem that becomes important much faster in real production environments: how do you make AI useful during an incident without losing control of the data being analysed?
