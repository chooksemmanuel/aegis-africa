# Architecture

## Phase 0 architecture

The Phase 0 prototype is intentionally local and simple.

```mermaid
flowchart TD
    U[User] --> UI[Streamlit app: prototype/app.py]
    UI --> D[Rule engine: prototype/detector.py]
    D --> M[Message-pattern checks]
    D --> R[URL-structure checks]
    M --> S[Weighted score and risk category]
    R --> S
    S --> O[Indicators, explanation, and safe guidance]

    N1[No external API] -.-> D
    N2[No database] -.-> D
    N3[No URL fetching] -.-> D
    N4[No AI or ML model] -.-> D
```

## Component responsibilities

### `prototype/app.py`

- Collects message text and an optional URL.
- Loads synthetic demonstration examples.
- Calls the detector and renders results.
- Handles expected validation errors and a generic unexpected-error state.
- Displays the educational-prototype disclaimer.

### `prototype/detector.py`

- Normalizes inputs.
- Extracts visible HTTP-style URLs from message text.
- Applies deterministic message and URL rules.
- Deduplicates indicators.
- Calculates a capped heuristic score.
- Produces risk wording and defensive guidance.

### `prototype/sample_messages.py`

- Contains fictional examples only.
- Provides no real customer, contact, or incident data.

### `tests/test_detector.py`

- Tests core rule behavior and input boundaries.
- Makes no network calls.

## Data flow and storage

The application processes inputs in memory. The repository does not implement a database, file-based input archive, analytics event, or application-level message log. A person deploying the app must still review hosting, reverse-proxy, platform, and infrastructure logs before making a privacy statement.

## Proposed future architecture - not implemented

```mermaid
flowchart LR
    C[Consented user channel] --> G[Authenticated API gateway]
    G --> V[Input validation and rate limiting]
    V --> P[Detection pipeline]
    P --> RR[Transparent rule engine]
    P --> REP[Optional reputation services]
    P --> ML[Optional evaluated ML model]
    RR --> E[Explainable result]
    REP --> E
    ML --> E
    E --> C

    P --> AL[Minimal audited security logs]
    DP[Consent, retention, and deletion controls] --> AL
    IR[Incident response and abuse controls] --> G
```

This future design is a planning sketch only. Each external service, data store, and platform integration would require security, privacy, legal, reliability, cost, and policy review.
