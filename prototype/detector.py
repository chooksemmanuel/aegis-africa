"""Rule-based message and URL screening for the Aegis Africa Phase 0 prototype.

This module performs local, deterministic checks. It does not call external
services, fetch URLs, train or run an AI model, or store user input.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import ipaddress
import re
from typing import Iterable
from urllib.parse import urlparse

MAX_MESSAGE_LENGTH = 20_000
MAX_URL_LENGTH = 2_048

URL_PATTERN = re.compile(
    r"(?i)\b(?:https?://|www\.)[^\s<>\[\]{}\"']+"
)

SHORTENER_DOMAINS = {
    "bit.ly",
    "cutt.ly",
    "is.gd",
    "rb.gy",
    "rebrand.ly",
    "shorturl.at",
    "t.co",
    "tinyurl.com",
}

LOOKALIKE_STYLE_PATTERNS = {
    "paypa1",
    "micr0soft",
    "g00gle",
    "whatsap",
    "faceb00k",
    "instagrarn",
    "paystak",
    "pa1mpay",
    "f1utterwave",
}

SUSPICIOUS_HOST_KEYWORDS = {
    "account",
    "confirm",
    "login",
    "payment",
    "secure",
    "support",
    "update",
    "verify",
    "wallet",
}


@dataclass(frozen=True)
class Indicator:
    """A single rule that contributed to the assessment."""

    code: str
    title: str
    detail: str
    weight: int
    source: str


@dataclass(frozen=True)
class Assessment:
    """Result returned by :func:`assess_content`."""

    score: int
    level: str
    summary: str
    indicators: tuple[Indicator, ...]
    guidance: tuple[str, ...]
    analyzed_urls: tuple[str, ...]
    disclaimer: str

    def to_dict(self) -> dict:
        """Return a JSON-friendly representation for interfaces or tests."""

        result = asdict(self)
        result["indicators"] = [asdict(item) for item in self.indicators]
        return result


def _indicator(
    code: str,
    title: str,
    detail: str,
    weight: int,
    source: str,
) -> Indicator:
    return Indicator(code=code, title=title, detail=detail, weight=weight, source=source)


def _contains_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def extract_urls(message: str) -> list[str]:
    """Extract and clean HTTP-style URLs from a message.

    The function does not open or resolve any URL.
    """

    found: list[str] = []
    for match in URL_PATTERN.findall(message or ""):
        cleaned = match.rstrip(".,;:!?)]}")
        if cleaned.lower().startswith("www."):
            cleaned = "https://" + cleaned
        if cleaned not in found:
            found.append(cleaned)
    return found


def _assess_message(message: str) -> list[Indicator]:
    text = message.strip()
    lowered = text.lower()
    indicators: list[Indicator] = []

    credential_patterns = [
        r"\bpasswords?\b",
        r"\bpasscodes?\b",
        r"\botp(?:s)?\b",
        r"\bone[- ]time (?:password|code)s?\b",
        r"\bpins?\b",
        r"\bverification codes?\b",
        r"\bsecurity codes?\b",
        r"\blogin (?:details|credentials)\b",
        r"\bcredentials?\b",
    ]
    if _contains_any(lowered, credential_patterns):
        indicators.append(
            _indicator(
                "credential_request",
                "Credential or verification-code request",
                "The message appears to request a password, PIN, OTP, or similar secret.",
                32,
                "message",
            )
        )

    payment_change_patterns = [
        r"\b(?:change|changed|update|updated|replace|revised|new)\b.{0,35}\b(?:bank|account|payment|transfer) (?:details?|number|information)\b",
        r"\b(?:send|transfer|pay|remit)\b.{0,35}\b(?:new|different|alternate) (?:account|wallet|number)\b",
        r"\baccount number (?:has|was) changed\b",
    ]
    if _contains_any(lowered, payment_change_patterns):
        indicators.append(
            _indicator(
                "payment_details_change",
                "Payment-detail change",
                "The message asks for money to be sent using new or changed payment details.",
                28,
                "message",
            )
        )

    payment_words = r"\b(?:pay|payment|transfer|invoice|bank|account|wallet|money|funds?)\b"
    urgency_words = r"\b(?:urgent|urgently|immediately|right now|act now|today|within \d+ (?:minutes?|hours?)|without delay|asap)\b"
    if re.search(payment_words, lowered) and re.search(urgency_words, lowered):
        indicators.append(
            _indicator(
                "urgent_payment",
                "Urgent payment pressure",
                "Payment language is combined with pressure to act quickly.",
                22,
                "message",
            )
        )

    threat_patterns = [
        r"\baccount (?:will be|has been|is) (?:blocked|closed|disabled|suspended|locked)\b",
        r"\bfinal warning\b",
        r"\blegal action\b",
        r"\bservice (?:will be|has been) terminated\b",
        r"\bfailure to (?:respond|pay|verify).{0,30}(?:suspension|closure|penalty|termination)\b",
    ]
    if _contains_any(lowered, threat_patterns):
        indicators.append(
            _indicator(
                "threat_pressure",
                "Threat or consequence pressure",
                "The message threatens account loss, penalties, or another immediate consequence.",
                18,
                "message",
            )
        )

    impersonation_terms = r"\b(?:ceo|director|manager|finance team|accounts department|bank support|customer care|supplier|vendor|administrator|it support)\b"
    request_terms = r"\b(?:send|share|pay|transfer|confirm|verify|provide|reply|click|open)\b"
    if re.search(impersonation_terms, lowered) and re.search(request_terms, lowered):
        indicators.append(
            _indicator(
                "impersonation_language",
                "Possible impersonation language",
                "The sender presents themselves as an authority, supplier, or support contact while making a request.",
                14,
                "message",
            )
        )

    off_channel_patterns = [
        r"\bdo not (?:call|contact|tell|inform)\b",
        r"\bkeep (?:this|it) confidential\b",
        r"\bmove (?:this|the conversation|the chat) to\b",
        r"\breply (?:only )?(?:to|on) (?:my )?(?:personal|private) (?:email|number|account)\b",
        r"\bdelete (?:this|the) message\b",
        r"\bavoid the official channel\b",
    ]
    if _contains_any(lowered, off_channel_patterns):
        indicators.append(
            _indicator(
                "off_channel_request",
                "Request to avoid an official channel",
                "The message asks for secrecy or movement away from a normal verification channel.",
                20,
                "message",
            )
        )

    unusual_payment_patterns = [
        r"\bgift cards?\b",
        r"\bprepaid vouchers?\b",
        r"\bcrypto(?:currency)?\b",
        r"\bbitcoin\b",
    ]
    if _contains_any(lowered, unusual_payment_patterns) and re.search(
        r"\b(?:buy|purchase|send|pay|transfer)\b", lowered
    ):
        indicators.append(
            _indicator(
                "unusual_payment_method",
                "Unusual payment method",
                "The message requests payment through a hard-to-reverse method.",
                20,
                "message",
            )
        )

    urgency_count = len(
        re.findall(
            r"\b(?:urgent|immediately|asap|now|today|quickly|hurry|final warning)\b",
            lowered,
        )
    )
    letters = [character for character in text if character.isalpha()]
    uppercase_ratio = (
        sum(character.isupper() for character in letters) / len(letters) if letters else 0.0
    )
    if text.count("!") >= 3 or urgency_count >= 3 or (len(letters) >= 20 and uppercase_ratio >= 0.55):
        indicators.append(
            _indicator(
                "excessive_urgency",
                "Excessive urgency or alarm",
                "The writing style uses repeated urgency, threats, capitalization, or exclamation marks.",
                10,
                "message",
            )
        )

    return indicators


def _normalize_url(raw_url: str) -> str:
    candidate = raw_url.strip()
    if not candidate:
        return ""
    if len(candidate) > MAX_URL_LENGTH:
        raise ValueError(f"URL exceeds the {MAX_URL_LENGTH:,}-character prototype limit.")
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", candidate):
        candidate = "https://" + candidate
    return candidate


def _assess_url(raw_url: str) -> tuple[str, list[Indicator]]:
    normalized = _normalize_url(raw_url)
    if not normalized:
        return "", []

    indicators: list[Indicator] = []
    parsed = urlparse(normalized)
    hostname = (parsed.hostname or "").lower().rstrip(".")

    if not hostname:
        indicators.append(
            _indicator(
                "invalid_url",
                "Unclear or incomplete URL",
                "The value could not be parsed as a normal web address.",
                12,
                "url",
            )
        )
        return normalized, indicators

    if parsed.scheme.lower() != "https":
        indicators.append(
            _indicator(
                "non_https_url",
                "URL does not use HTTPS",
                "The address uses an unencrypted or unusual URL scheme.",
                8,
                "url",
            )
        )

    try:
        ipaddress.ip_address(hostname.strip("[]"))
    except ValueError:
        pass
    else:
        indicators.append(
            _indicator(
                "raw_ip_url",
                "Raw IP address in URL",
                "The URL uses an IP address instead of a recognizable domain name.",
                24,
                "url",
            )
        )

    if hostname in SHORTENER_DOMAINS or any(
        hostname.endswith("." + domain) for domain in SHORTENER_DOMAINS
    ):
        indicators.append(
            _indicator(
                "shortened_url",
                "Shortened URL",
                "The destination is hidden behind a link-shortening service.",
                18,
                "url",
            )
        )

    if "xn--" in hostname:
        indicators.append(
            _indicator(
                "punycode_domain",
                "Internationalized or punycode domain",
                "The hostname uses encoded characters that can sometimes be used in lookalike domains.",
                22,
                "url",
            )
        )

    if parsed.username or "@" in parsed.netloc:
        indicators.append(
            _indicator(
                "userinfo_in_url",
                "User information embedded in URL",
                "Text before an @ symbol can obscure the actual destination host.",
                20,
                "url",
            )
        )

    labels = [label for label in hostname.split(".") if label]
    if len(labels) >= 5:
        indicators.append(
            _indicator(
                "many_subdomains",
                "Unusually deep subdomain structure",
                "The URL contains many domain levels, which can make the true destination harder to identify.",
                10,
                "url",
            )
        )

    if len(hostname) >= 50:
        indicators.append(
            _indicator(
                "long_hostname",
                "Unusually long hostname",
                "A very long hostname can be used to hide the important part of a destination.",
                8,
                "url",
            )
        )

    if hostname.count("-") >= 3:
        indicators.append(
            _indicator(
                "hyphen_heavy_domain",
                "Hyphen-heavy domain",
                "The hostname contains several hyphens, a pattern sometimes seen in imitation login pages.",
                8,
                "url",
            )
        )

    compact_hostname = re.sub(r"[^a-z0-9]", "", hostname)
    if any(pattern in compact_hostname for pattern in LOOKALIKE_STYLE_PATTERNS):
        indicators.append(
            _indicator(
                "lookalike_spelling",
                "Lookalike-style spelling",
                "The hostname contains a common letter/number substitution or misspelling pattern.",
                24,
                "url",
            )
        )
    elif any(label_has_letter_digit_mix(label) for label in labels):
        indicators.append(
            _indicator(
                "mixed_character_domain",
                "Mixed letters and digits in domain label",
                "A domain label mixes letters and digits in a way that may imitate another name.",
                10,
                "url",
            )
        )

    keyword_hits = {
        keyword
        for keyword in SUSPICIOUS_HOST_KEYWORDS
        if keyword in re.split(r"[.\-_]", hostname)
    }
    if len(keyword_hits) >= 2:
        indicators.append(
            _indicator(
                "credential_theme_domain",
                "Verification-themed domain wording",
                "The hostname combines multiple words such as login, verify, secure, account, or payment.",
                12,
                "url",
            )
        )

    return normalized, indicators


def label_has_letter_digit_mix(label: str) -> bool:
    """Return True for a domain label with a suspicious letter/digit mixture."""

    return (
        bool(re.search(r"[a-z]", label))
        and bool(re.search(r"\d", label))
        and bool(re.search(r"[01357]", label))
    )


def _deduplicate(indicators: Iterable[Indicator]) -> list[Indicator]:
    seen: set[tuple[str, str]] = set()
    unique: list[Indicator] = []
    for item in indicators:
        key = (item.code, item.source)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def _risk_level(score: int) -> tuple[str, str]:
    if score >= 60:
        return "High", "Multiple indicators suggest that the content should not be trusted without independent verification."
    if score >= 30:
        return "Caution", "The content contains one or more warning signs that deserve verification before action."
    return "Low", "Few or no configured warning signs were detected, but the content is not proven safe."


def _build_guidance(indicators: Iterable[Indicator]) -> list[str]:
    codes = {item.code for item in indicators}
    guidance = [
        "Do not click links, download files, reply, or send money until the request is verified.",
        "Verify through a trusted contact method you already know, such as an official app, saved phone number, or manually typed website.",
    ]

    if "credential_request" in codes:
        guidance.append("Never share passwords, PINs, OTPs, recovery codes, or authentication codes with another person.")
    if {"payment_details_change", "urgent_payment", "unusual_payment_method"} & codes:
        guidance.append("Confirm payment-detail changes verbally with the known supplier or recipient before transferring funds.")
    if any(item.source == "url" for item in indicators):
        guidance.append("Inspect the destination carefully. This prototype does not open the link or check live reputation data.")
    if {"off_channel_request", "impersonation_language"} & codes:
        guidance.append("Contact the claimed person or organization independently instead of using contact details supplied in the message.")

    guidance.extend(
        [
            "If credentials were already shared, change them immediately and enable multi-factor authentication where available.",
            "If money was already sent, contact the bank or payment provider promptly and preserve the message as evidence.",
        ]
    )
    return guidance


def assess_content(message: str = "", url: str = "") -> Assessment:
    """Assess message text and optional URL using local defensive rules.

    Args:
        message: Suspicious message text. Maximum 20,000 characters.
        url: Optional URL. Maximum 2,048 characters.

    Raises:
        ValueError: If both inputs are empty or either exceeds the prototype limit.
    """

    message = message or ""
    url = url or ""
    if not message.strip() and not url.strip():
        raise ValueError("Enter a message, a URL, or both.")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError(f"Message exceeds the {MAX_MESSAGE_LENGTH:,}-character prototype limit.")

    indicators: list[Indicator] = []
    if message.strip():
        indicators.extend(_assess_message(message))

    urls = extract_urls(message)
    if url.strip():
        urls.append(url.strip())

    normalized_urls: list[str] = []
    for candidate in urls:
        normalized, url_indicators = _assess_url(candidate)
        if normalized and normalized not in normalized_urls:
            normalized_urls.append(normalized)
        indicators.extend(url_indicators)

    unique_indicators = _deduplicate(indicators)
    score = min(100, sum(item.weight for item in unique_indicators))
    level, summary = _risk_level(score)

    return Assessment(
        score=score,
        level=level,
        summary=summary,
        indicators=tuple(unique_indicators),
        guidance=tuple(_build_guidance(unique_indicators)),
        analyzed_urls=tuple(normalized_urls),
        disclaimer=(
            "Educational Phase 0 prototype only. A low score does not prove safety, and a high score is not a legal or technical determination of fraud."
        ),
    )
