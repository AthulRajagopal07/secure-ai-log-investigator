import re
from pathlib import Path

INPUT_FILE = Path("logs/raw_app.log")
OUTPUT_FILE = Path("logs/sanitized_app.log")


PATTERNS = {
    "PRIVATE_KEY": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?"
        r"-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        re.IGNORECASE | re.DOTALL,
    ),
    "AUTHORIZATION": re.compile(
        r"Authorization\s*[:=]\s*Bearer\s+[A-Za-z0-9._-]+",
        re.IGNORECASE,
    ),
    "JWT": re.compile(
        r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
    ),
    "AWS_ACCESS_KEY": re.compile(
        r"\bAKIA[0-9A-Z]{16}\b"
    ),
    "EMAIL": re.compile(
        r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+\b"
    ),
    "IP": re.compile(
        r"\b(?:"
        r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\."
        r"){3}"
        r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b"
    ),
    "PHONE": re.compile(
        r"\b(?:\+?\d[\d\s().-]{8,}\d)\b"
    ),
    "PASSWORD": re.compile(
        r"(?i)\b(password|passwd|pwd)\s*[:=]\s*[^\s,;]+"
    ),
    "TOKEN": re.compile(
        r"\b(?:"
        r"sk_live_[A-Za-z0-9_-]+|"
        r"ghp_[A-Za-z0-9]+|"
        r"api-token-[A-Za-z0-9_-]+|"
        r"Bearer\s+[A-Za-z0-9._-]+"
        r")\b",
        re.IGNORECASE,
    ),
    "REQUEST_ID": re.compile(
        r"\breq-\d+\b"
    ),
    "INTERNAL_HOST": re.compile(
        r"\b[a-zA-Z0-9-]+\.internal\.local\b"
    ),
}


def sanitize_line(line: str) -> str:
    """Redact known sensitive patterns from a single log line."""

    sanitized = line

    for label, pattern in PATTERNS.items():
        sanitized = pattern.sub(f"[{label}]", sanitized)

    return sanitized


def sanitize_file() -> None:
    """Sanitize the complete raw log file."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"{INPUT_FILE} does not exist. "
            "Run generate_logs.py first."
        )

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with (
        INPUT_FILE.open("r", encoding="utf-8") as infile,
        OUTPUT_FILE.open("w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            outfile.write(sanitize_line(line))

    print(f"Sanitized log written to {OUTPUT_FILE}")


if __name__ == "__main__":
    sanitize_file()