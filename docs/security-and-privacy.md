# Security and privacy

## Scope

This document describes the Phase 0 repository. It is not a production security assessment or compliance statement.

## Current controls

- The detector is defensive and read-only.
- It does not generate phishing content or collect credentials.
- It does not open submitted URLs.
- It makes no external API, DNS, reputation, email, messaging, bank, or payment-platform request.
- It does not implement a database or application-level input log.
- Repository examples are synthetic.
- Input lengths are bounded to reduce accidental misuse and resource exhaustion.
- Expected input errors are handled without exposing stack traces in the interface.

## Data handling

Inputs are processed in the memory of the running Python process. The application code does not intentionally persist them. This does not guarantee that every hosting layer is log-free. Before any hosted deployment, review:

- Streamlit hosting behavior.
- Reverse-proxy and web-server logs.
- Cloud platform logs and diagnostics.
- Crash reporting and analytics.
- Backups and snapshots.
- Administrative access.
- Data location and cross-border transfer implications.

## User guidance

Do not paste the following into a public or unapproved hosted copy:

- Passwords, PINs, OTPs, recovery codes, or authentication tokens.
- Bank-account or card details.
- Government identifiers.
- Confidential customer or employee information.
- Private messages without permission.
- Active incident evidence that must be handled under a formal response process.

## Accuracy and decision risk

The rules can produce false positives and false negatives. A low score does not prove safety, and a high score does not prove fraud. The app should support a pause-and-verify decision, not replace independent verification, incident response, legal advice, or a professional security product.

## Threat considerations for a future hosted version

A future system would need to address:

- Malicious or oversized input.
- Stored cross-site scripting and unsafe rendering.
- URL-fetching risks, including server-side request forgery, redirects, and dangerous content.
- Authentication, authorization, account recovery, and session security.
- Abuse, automation, rate limiting, denial of service, and scraping.
- Secret management and dependency vulnerabilities.
- Sensitive logging and excessive data retention.
- Insider access and administrative audit trails.
- Tenant separation.
- Availability, backups, and disaster recovery.
- Vulnerability disclosure and incident response.
- Platform-policy and legal requirements in each operating market.

## Requirements before collecting real examples

1. Define a specific research purpose.
2. Obtain informed consent.
3. Minimize data at collection.
4. Remove direct and indirect identifiers.
5. Separate identity and research records.
6. Define retention and deletion periods.
7. Restrict access and maintain an audit trail.
8. Establish a lawful and ethical basis for use.
9. Prevent examples from becoming a phishing or impersonation resource.
10. Document who can approve secondary use or model training.

## Responsible development boundary

This repository must remain focused on defensive detection, verification, and education. It must not add credential capture, message impersonation, phishing generation, unauthorized account access, offensive testing against third parties, or evasion guidance.
