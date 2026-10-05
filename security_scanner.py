import re
import sys
from pathlib import Path

FILES_TO_SCAN = [
    Path("logs/sanitized_app.log"),
    Path("reports/incident_summary.md"),
]


PATTERNS = {
    "EMAIL": re.compile(
        r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+\b"
    ),
    "IP": re.compile(
        r"\b(?:"
        r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\."
        r"){3}"
        r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"
    ),
    "JWT": re.compile(
        r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
    ),
    "AWS_ACCESS_KEY": re.compile(
        r"\bAKIA[0-9A-Z]{16}\b"
    ),
    "TOKEN": re.compile(
        r"\b(?:"
        r"sk_live_[A-Za-z0-9_-]+|"
        r"ghp_[A-Za-z0-9]+|"
        r"api-token-[A-Za-z0-9_-]+"
        r")\b",
        re.IGNORECASE,
    ),
    "AUTHORIZATION": re.compile(
        r"Authorization\s*[:=]\s*Bearer\s+[A-Za-z0-9._-]+",
        re.IGNORECASE,
    ),
    "PASSWORD": re.compile(
        r"(?i)\b(password|passwd|pwd)\s*[:=]\s*[^\s,;]+"
    ),
    "PRIVATE_KEY": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        re.IGNORECASE,
    ),
}


def scan_text(text: str) -> dict[str, list[str]]:
    """Return all detected sensitive values grouped by type."""

    findings: dict[str, list[str]] = {}

    for label, pattern in PATTERNS.items():
        matches = pattern.findall(text)

        if matches:
            findings[label] = matches

    return findings


def scan_files(paths: list[Path]) -> dict[str, int]:
    """Scan files and return counts of sensitive findings."""

    counts: dict[str, int] = {}

    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        text = path.read_text(encoding="utf-8")
        findings = scan_text(text)

        for label, matches in findings.items():
            counts[label] = counts.get(label, 0) + len(matches)

    return counts


def security_gate(paths: list[Path]) -> bool:
    """
    Return True only when no detectable sensitive information remains.
    """

    counts = scan_files(paths)

    print("\nSECURITY GATE")
    print("=============")

    if not counts:
        print("Status: PASS")
        print("No detectable sensitive information remains.")
        return True

    print("Status: FAIL")
    print("Sensitive information was detected:")

    for label, count in sorted(counts.items()):
        print(f"  {label}: {count}")

    print("\nAI analysis is BLOCKED.")
    print("Review and improve the sanitization rules before continuing.")

    return False


def main() -> None:
    try:
        passed = security_gate(FILES_TO_SCAN)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()