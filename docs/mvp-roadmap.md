# MVP roadmap

The roadmap uses evidence gates rather than dates or promised outcomes.

## Phase 0 - concept documentation and local prototype

**Purpose:** Create a truthful technical starting point.

- Document the original problem and product hypotheses.
- Build a rule-based message and URL screening prototype.
- Use synthetic examples only.
- Add automated tests for deterministic behavior.
- Identify unsupported claims from the pitch.
- Avoid platform integration, live scanning, customer data, and AI claims.

**Exit evidence:** Repository runs locally, tests pass, limitations are documented, and public claims match the implementation.

## Phase 1 - structured problem validation

**Purpose:** Determine whether the proposed problem, user, and workflow are sufficiently specific.

- Conduct structured interviews with African small-business owners.
- Separate outreach sent from conversations completed.
- Identify recurring scam categories and operational workflows.
- Understand current verification methods and failure points.
- Refine the target segment, language needs, and primary use case.
- Obtain permission before publishing any quotation or identifying detail.

**Exit evidence:** A documented pattern across multiple completed conversations, a defined primary user, and a prioritized use case. No minimum interview number is claimed in advance.

## Phase 2 - limited MVP

**Purpose:** Test a narrowly defined solution against a validated workflow.

- Build only the features required by the primary use case.
- Explore official WhatsApp Business Platform integration if the use case requires it.
- Define authentication, consent, retention, deletion, and support processes.
- Create a consented evaluation dataset or controlled test set.
- Measure detection accuracy, false-positive rates, false negatives, and user comprehension.
- Add monitoring, secure configuration, dependency management, and abuse controls.

**Exit evidence:** Reproducible test results, documented security and privacy controls, and evidence that intended users understand and benefit from the workflow.

## Phase 3 - regional data and model evaluation

**Purpose:** Determine whether additional detection methods create measurable value.

- Collect properly consented and anonymized regional threat examples.
- Establish data-quality, labeling, and governance procedures.
- Compare rules, external reputation signals, and machine-learning approaches.
- Add machine learning only if it improves a defined metric without unacceptable privacy, bias, explainability, or maintenance costs.
- Explore limited pilots or distribution relationships only after validation.

**Exit evidence:** A documented evaluation, approved data-handling process, and a clearly scoped pilot proposal. A discussion with a company is not a partnership unless formally agreed and publicly disclosable.

## Explicit non-goals for the current phase

- Claiming production readiness.
- Training a model merely to support an AI label.
- Collecting private messages without consent.
- Scraping threat data of uncertain provenance.
- Building unofficial automation against messaging or financial platforms.
- Optimizing for user counts, revenue, or publicity before problem validation.
