"""Streamlit interface for the Aegis Africa Phase 0 prototype."""

from __future__ import annotations

import streamlit as st

try:
    # Package import for tests and module execution.
    from prototype.detector import assess_content
    from prototype.sample_messages import SAMPLE_MESSAGES
except ModuleNotFoundError:
    # Local import used by `streamlit run prototype/app.py`.
    from detector import assess_content
    from sample_messages import SAMPLE_MESSAGES


def _render_indicator(item) -> None:
    st.markdown(f"**{item.title}**  ")
    st.caption(f"{item.detail} · Source: {item.source} · Rule weight: {item.weight}")


def main() -> None:
    st.set_page_config(
        page_title="Aegis Africa - Phase 0",
        page_icon="🛡️",
        layout="centered",
    )

    st.title("🛡️ Aegis Africa")
    st.subheader("Phase 0 message and URL risk screener")
    st.info(
        "This is an educational, rule-based prototype. It does not use an AI model, "
        "open links, query threat-intelligence services, or replace professional cybersecurity tools."
    )

    sample_name = st.selectbox(
        "Load a synthetic example",
        ["Start with empty fields", *SAMPLE_MESSAGES.keys()],
    )
    sample = SAMPLE_MESSAGES.get(sample_name, {"message": "", "url": ""})

    message = st.text_area(
        "Suspicious message",
        value=sample["message"],
        height=180,
        max_chars=20_000,
        placeholder="Paste a suspicious SMS, email, or chat message here...",
    )
    url = st.text_input(
        "Optional URL",
        value=sample["url"],
        max_chars=2_048,
        placeholder="https://example.com",
    )

    st.caption("The application code does not call external services or intentionally persist submitted content.")

    if st.button("Assess risk", type="primary", use_container_width=True):
        try:
            result = assess_content(message=message, url=url)
        except ValueError as exc:
            st.warning(str(exc))
            return
        except Exception:
            st.error("The prototype could not complete the assessment. Clear the fields and try again.")
            return

        if result.level == "High":
            st.error(f"Risk level: {result.level} · Score: {result.score}/100")
        elif result.level == "Caution":
            st.warning(f"Risk level: {result.level} · Score: {result.score}/100")
        else:
            st.success(f"Risk level: {result.level} · Score: {result.score}/100")

        st.write(result.summary)

        st.markdown("### Triggered indicators")
        if result.indicators:
            for indicator in result.indicators:
                _render_indicator(indicator)
        else:
            st.write("No configured warning indicators were triggered.")

        if result.analyzed_urls:
            st.markdown("### URLs reviewed")
            for reviewed_url in result.analyzed_urls:
                st.code(reviewed_url, language=None)

        st.markdown("### Safe next steps")
        for step in result.guidance:
            st.markdown(f"- {step}")

        st.caption(result.disclaimer)

    with st.expander("What this prototype does not do"):
        st.markdown(
            """
- It does not visit or scan a website.
- It does not check domain age, DNS records, malware feeds, or live reputation services.
- It does not authenticate a sender or prove that a message is safe or fraudulent.
- It does not integrate with WhatsApp, email accounts, banks, or payment platforms.
- It does not contain a trained machine-learning or artificial-intelligence model.
"""
        )


if __name__ == "__main__":
    main()
