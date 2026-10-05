from security_scanner import scan_text


def test_raw_email_fails_security_scan():
    findings = scan_text(
        "user=john@example.com"
    )

    assert "EMAIL" in findings


def test_raw_token_fails_security_scan():
    findings = scan_text(
        "token=api-token-test"
    )

    assert "TOKEN" in findings


def test_sanitized_values_are_safe():
    findings = scan_text(
        "user=[EMAIL] ip=[IP] token=[TOKEN]"
    )

    assert findings == {}


def test_private_key_is_detected():
    findings = scan_text(
        "-----BEGIN PRIVATE KEY-----"
    )

    assert "PRIVATE_KEY" in findings