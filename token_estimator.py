from pathlib import Path

RAW_FILE = Path("logs/raw_app.log")
SANITIZED_FILE = Path("logs/sanitized_app.log")
SUMMARY_FILE = Path("reports/incident_summary.md")


def estimate_tokens(text: str) -> int:
    """
    Approximate token count.

    This is intentionally an estimate rather than an exact model
    tokenizer count. Different LLMs use different tokenizers.
    """

    if not text:
        return 0

    return max(1, len(text) // 4)


def file_stats(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist."
        )

    text = path.read_text(encoding="utf-8")

    return {
        "file": str(path),
        "characters": len(text),
        "estimated_tokens": estimate_tokens(text),
        "lines": text.count("\n"),
    }


def print_stats(stats: dict) -> None:
    print(f"File: {stats['file']}")
    print(f"Lines: {stats['lines']}")
    print(f"Characters: {stats['characters']}")
    print(
        f"Estimated tokens: "
        f"{stats['estimated_tokens']}"
    )
    print()


def main() -> None:
    raw_stats = file_stats(RAW_FILE)
    sanitized_stats = file_stats(SANITIZED_FILE)
    summary_stats = file_stats(SUMMARY_FILE)

    print("\nTOKEN USAGE COMPARISON")
    print("======================\n")

    print_stats(raw_stats)
    print_stats(sanitized_stats)
    print_stats(summary_stats)

    raw_tokens = raw_stats["estimated_tokens"]
    summary_tokens = summary_stats["estimated_tokens"]

    reduction = 100 - (
        summary_tokens / raw_tokens * 100
    )

    print(
        "Estimated token reduction from raw log "
        f"to incident summary: {reduction:.2f}%"
    )

    print(
        "\nNOTE: Token counts are approximate. "
        "Actual tokenization depends on the model."
    )


if __name__ == "__main__":
    main()