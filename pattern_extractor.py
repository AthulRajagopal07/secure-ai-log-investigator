import re
from collections import Counter
from pathlib import Path

INPUT_FILE = Path("logs/sanitized_app.log")
REPORT_DIR = Path("reports")
REPORT_FILE = REPORT_DIR / "incident_summary.md"

IMPORTANT_LEVELS = ["ERROR", "CRITICAL", "WARNING"]


def normalize_log_line(line: str) -> str:
    """
    Normalize dynamic values so similar incidents can be grouped.
    """

    line = re.sub(
        r"^\d{4}-\d{2}-\d{2}.*?\s(INFO|WARNING|ERROR|CRITICAL)\s",
        "",
        line,
    )

    line = re.sub(
        r"request_id=\[REQUEST_ID\]",
        "request_id=[REQUEST_ID]",
        line,
    )

    return line.strip()


def extract_patterns() -> Counter:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"{INPUT_FILE} does not exist. "
            "Run sanitizer.py first."
        )

    counter = Counter()

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if any(
                level in line
                for level in IMPORTANT_LEVELS
            ):
                normalized = normalize_log_line(line)
                counter[normalized] += 1

    return counter


def calculate_level_counts() -> Counter:
    counts = Counter()

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            for level in IMPORTANT_LEVELS:
                if level in line:
                    counts[level] += 1
                    break

    return counts


def write_report(counter: Counter) -> None:
    REPORT_DIR.mkdir(exist_ok=True)

    total_events = sum(counter.values())
    level_counts = calculate_level_counts()
    top_patterns = counter.most_common(20)

    with REPORT_FILE.open("w", encoding="utf-8") as report:
        report.write("# Incident Log Pattern Summary\n\n")

        report.write("## Incident Metrics\n\n")
        report.write(
            f"- Total important events: {total_events}\n"
        )
        report.write(
            f"- Critical events: {level_counts['CRITICAL']}\n"
        )
        report.write(
            f"- Error events: {level_counts['ERROR']}\n"
        )
        report.write(
            f"- Warning events: {level_counts['WARNING']}\n\n"
        )

        report.write("## Top Log Patterns\n\n")

        for pattern, count in top_patterns:
            report.write(f"### Occurrences: {count}\n")
            report.write("```text\n")
            report.write(pattern + "\n")
            report.write("```\n\n")

    print(f"Incident summary written to {REPORT_FILE}")


def main() -> None:
    patterns = extract_patterns()

    write_report(patterns)

    print("\nTop 5 patterns:\n")

    for pattern, count in patterns.most_common(5):
        print(f"{count}x - {pattern[:140]}")


if __name__ == "__main__":
    main()