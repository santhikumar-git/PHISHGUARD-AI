
import streamlit as st
import re

st.set_page_config(
    page_title="PHISHGUARD AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ PHISHGUARD AI")
st.subheader("Email Security & Phishing Risk Analysis")
st.caption("Educational cybersecurity prototype")

st.info(
    "This prototype uses simple detection rules. "
    "Its score is not a probability or proof of phishing."
)

SUSPICIOUS_PHRASES = [
    "verify your account",
    "urgent action required",
    "account will be suspended",
    "confirm your password",
    "claim your prize",
    "update your payment",
    "unusual login activity",
    "click immediately"
]


def analyze_email(email):
    score = 0
    findings = []
    text = email.lower()

    for phrase in SUSPICIOUS_PHRASES:
        if phrase in text:
            score += 15
            findings.append(f"Suspicious phrase: {phrase}")

    if re.search(r"\b(urgent|immediately|now)\b", text):
        score += 10
        findings.append("Urgent language detected")

    urls = re.findall(
        r"https?://[^\s<>\"']+|www\.[^\s<>\"']+",
        email,
        flags=re.IGNORECASE
    )

    if urls:
        score += 10
        findings.append("Contains a link that needs verification")

    if "password" in text or "login credentials" in text:
        score += 20
        findings.append("Sensitive account information mentioned")

    score = min(score, 100)

    if score >= 60:
        risk = "HIGH RISK"
    elif score >= 30:
        risk = "MEDIUM RISK"
    else:
        risk = "LOW RISK"

    if not findings:
        findings.append("No configured warning patterns detected")

    return score, risk, findings


st.divider()

st.header("📧 Email Scanner")

email_text = st.text_area(
    "Paste sample email text here",
    height=200,
    placeholder="Enter a sample email for analysis..."
)

if st.button("🔍 Analyse Email", type="primary"):
    if not email_text.strip():
        st.warning("Please enter some email text.")
    else:
        score, risk, findings = analyze_email(email_text)

        st.subheader("Analysis Results")

        col1, col2 = st.columns(2)
        col1.metric("Risk Score", f"{score}/100")
        col2.metric("Risk Category", risk)

        st.subheader("Detection Findings")

        for finding in findings:
            st.write("•", finding)

        st.warning(
            "Never click suspicious links or enter passwords. "
            "Verify important requests through a trusted channel."
        )

        st.caption(
            "This rule-based score is a heuristic indicator, "
            "not a calibrated probability or definitive verdict."
        )

st.divider()
st.caption("PHISHGUARD AI | Version 1.0 | Educational Project")
