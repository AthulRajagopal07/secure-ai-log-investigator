from pattern_extractor import normalize_log_line


def test_timestamp_is_removed():
    line = (
        "2026-10-05 01:00:00 ERROR "
        "service=payment-api "
        "message='Database timeout'"
    )

    result = normalize_log_line(line)

    assert not result.startswith("2026-10-05")
    assert "Database timeout" in result