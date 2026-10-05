from token_estimator import estimate_tokens


def test_empty_text_has_zero_tokens():
    assert estimate_tokens("") == 0


def test_token_estimate_is_positive():
    result = estimate_tokens(
        "This is a production log message."
    )

    assert result > 0