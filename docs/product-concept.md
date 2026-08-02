# Product concept

## Original March 2026 vision

The competition pitch proposed a mobile-first cybersecurity service for African small businesses with three possible components:

1. A WhatsApp-oriented security assistant for suspicious messages and links.
2. Email-fraud monitoring focused on invoice and impersonation risks.
3. Short security-awareness lessons for non-technical teams.

The pitch also discussed a possible low-cost subscription and future distribution through financial-technology channels. These were product and business-model hypotheses, not implemented features, customer commitments, or partnerships.

## Current August 2026 implementation

The repository currently contains one small Phase 0 application:

- A Python and Streamlit interface.
- A local, deterministic rules engine.
- Message checks for urgency, changed payment details, credential requests, threats, impersonation language, and off-channel requests.
- URL checks for shorteners, raw IP addresses, punycode, embedded user information, unusual domain structure, and illustrative lookalike patterns.
- Explanations for each triggered rule.
- Defensive next-step guidance.
- Synthetic examples and automated tests.

## Product boundary

The current prototype is a learning and validation tool. It is not:

- A WhatsApp bot.
- An email-monitoring service.
- An endpoint-security product.
- A bank or payment-platform integration.
- An automated fraud adjudication system.
- An AI model trained on African threat data.
- A customer-ready subscription service.

## Design principles

- **Truthful status:** Clearly distinguish concept, prototype, validation, MVP, pilot, and production.
- **Explainability:** Show users the rules that produced a warning.
- **Data minimization:** Avoid collecting or retaining sensitive content without a defined need and consent process.
- **Defensive use:** Support detection, verification, and awareness only.
- **Mobile-first usability:** Keep the interaction simple enough for small-screen use, while validating actual user needs before platform integration.
- **Evidence before complexity:** Add machine learning only if measured evidence shows that it improves outcomes over transparent rules.
