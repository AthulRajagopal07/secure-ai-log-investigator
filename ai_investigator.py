import shutil
import subprocess
import sys
from pathlib import Path

from security_scanner import security_gate

SUMMARY_FILE = Path("reports/incident_summary.md")
AI_REPORT_FILE = Path("reports/ai_investigation.md")

AI_INPUT_FILES = [
    Path("logs/sanitized_app.log"),
    SUMMARY_FILE,
]


def build_prompt(summary: str) -> str:
    return f"""
You are a senior Site Reliability Engineer investigating a production incident.

Analyze ONLY the evidence provided below.

Important rules:
- Do not invent facts.
- Do not invent services.
- Do not invent infrastructure components.
- Do not assume a root cause without evidence.
- Clearly separate evidence from inference.
- Treat the confidence value as an engineering assessment, not a probability.
- Provide practical investigation commands.
- Clearly state what a human engineer must verify.
- Never recommend destructive commands.

Return the answer using this structure:

# AI Incident Investigation

## 1. Incident Summary

## 2. Severity Assessment

## 3. Most Likely Root Cause

## 4. Evidence From Logs

## 5. Affected Services

## 6. Recommended Investigation Commands

## 7. Recommended Remediation

## 8. AI Confidence Assessment

## 9. Human Validation Required

## 10. Limitations

Incident evidence:

{summary}
"""


def ask_ollama(prompt: str) -> str:
    if shutil.which("ollama") is None:
        raise RuntimeError(
            "Ollama is not installed or is not available in PATH. "
            "Install Ollama and run 'ollama pull mistral'."
        )

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        text=True,
        capture_output=True,
        check=False,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Ollama returned an error:\n\n"
            f"{result.stderr}"
        )

    return result.stdout.strip()


def main() -> None:
    if not SUMMARY_FILE.exists():
        raise FileNotFoundError(
            "Run pattern_extractor.py first."
        )

    print("Running security gate before AI analysis...")

    if not security_gate(AI_INPUT_FILES):
        print("\nAI investigation aborted.")
        sys.exit(1)

    summary = SUMMARY_FILE.read_text(encoding="utf-8")

    prompt = build_prompt(summary)

    print("\nSecurity gate passed.")
    print("Sending sanitized + aggregated evidence to local Mistral...")

    response = ask_ollama(prompt)

    AI_REPORT_FILE.parent.mkdir(exist_ok=True)
    AI_REPORT_FILE.write_text(
        response + "\n",
        encoding="utf-8",
    )

    print(f"\nAI investigation report written to {AI_REPORT_FILE}")
    print("\n--- AI RESPONSE ---\n")
    print(response)


if __name__ == "__main__":
    main()