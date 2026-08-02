"""Tests for the deterministic Phase 0 detection rules."""

import pytest

from prototype.detector import assess_content, extract_urls


def indicator_codes(result):
    return {item.code for item in result.indicators}


def test_requires_at_least_one_input():
    with pytest.raises(ValueError, match="Enter a message"):
        assess_content()


def test_neutral_message_is_low_risk():
    result = assess_content("Please review tomorrow's meeting agenda when convenient.")
    assert result.level == "Low"
    assert result.score == 0
    assert result.indicators == ()


def test_changed_payment_details_and_urgency_raise_risk():
    result = assess_content(
        "URGENT: Our bank account number has changed. Transfer today's invoice immediately to the new account."
    )
    codes = indicator_codes(result)
    assert "payment_details_change" in codes
    assert "urgent_payment" in codes
    assert result.level == "High"


def test_credential_request_is_detected():
    result = assess_content("Customer care needs your OTP and PIN to verify the account.")
    assert "credential_request" in indicator_codes(result)
    assert result.score >= 30


def test_official_channel_avoidance_is_detected():
    result = assess_content("Keep this confidential and do not call the office. Reply to my personal email.")
    assert "off_channel_request" in indicator_codes(result)


def test_shortened_url_is_detected_without_network_access():
    result = assess_content(url="https://bit.ly/example-placeholder")
    assert "shortened_url" in indicator_codes(result)
    assert result.analyzed_urls == ("https://bit.ly/example-placeholder",)


def test_raw_ip_and_http_are_detected():
    result = assess_content(url="http://192.0.2.10/verify")
    codes = indicator_codes(result)
    assert "raw_ip_url" in codes
    assert "non_https_url" in codes


def test_punycode_domain_is_detected():
    result = assess_content(url="https://xn--example-9db.invalid/login")
    assert "punycode_domain" in indicator_codes(result)


def test_lookalike_spelling_is_detected():
    result = assess_content(url="https://micr0soft-support.example.com")
    assert "lookalike_spelling" in indicator_codes(result)


def test_urls_are_extracted_from_message():
    message = "Please verify at https://secure-login-verify-account.example.com/update now."
    assert extract_urls(message) == ["https://secure-login-verify-account.example.com/update"]
    result = assess_content(message)
    assert result.analyzed_urls
    assert "credential_theme_domain" in indicator_codes(result)


def test_score_is_capped_at_100():
    result = assess_content(
        "URGENT FINAL WARNING!!! I am the bank support director. Your account will be suspended today. "
        "Send your OTP, password and PIN immediately, transfer payment to the new account, keep this confidential, "
        "do not call, and buy gift cards.",
        "http://192.0.2.10/secure-login-verify-account",
    )
    assert result.score == 100
    assert result.level == "High"


def test_message_length_limit():
    with pytest.raises(ValueError, match="20,000"):
        assess_content("x" * 20_001)


def test_url_length_limit():
    with pytest.raises(ValueError, match="2,048"):
        assess_content(url="https://" + "a" * 2_050)
