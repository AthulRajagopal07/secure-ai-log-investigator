from sanitizer import sanitize_line


def test_email_is_redacted():
    result = sanitize_line(
        "user=john@example.com"
    )

    assert "john@example.com" not in result
    assert "[EMAIL]" in result


def test_ip_is_redacted():
    result = sanitize_line(
        "ip=10.10.12.5"
    )

    assert "10.10.12.5" not in result
    assert "[IP]" in result


def test_token_is_redacted():
    result = sanitize_line(
        "token=api-token-demo"
    )

    assert "api-token-demo" not in result
    assert "[TOKEN]" in result


def test_password_is_redacted():
    result = sanitize_line(
        "password=SuperSecret123"
    )

    assert "SuperSecret123" not in result
    assert "[PASSWORD]" in result


def test_authorization_header_is_redacted():
    result = sanitize_line(
        "Authorization: Bearer abc.def.ghi"
    )

    assert "abc.def.ghi" not in result
    assert "[AUTHORIZATION]" in result