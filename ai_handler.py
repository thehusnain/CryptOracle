# pyrefly: ignore [missing-import]
from groq import Groq

# pyrefly: ignore [missing-import]
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def classify_message(message):
    prompt = f"""
    Analyze this message and classify it.

    Message: {message}

    Reply with ONLY one word from these options:
    communication / password / confidential
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip().lower()


def recommend_method(message, msg_type):
    """
    Deterministic rule-based recommendation — no AI involved.
    Rules are evaluated in order; first match wins.
    """
    import re

    text = message.strip()

    # Rule 1 — only digits
    if re.fullmatch(r"\d+", text):
        return "ROT5"

    # Rule 2 — only letters (no digits, no symbols), short
    if re.fullmatch(r"[a-zA-Z\s]+", text) and len(text) <= 40:
        return "ROT13"

    # Rule 3 — only letters, long
    if re.fullmatch(r"[a-zA-Z\s]+", text) and len(text) > 40:
        return "ROT47"

    # Rule 4 — contains punctuation or special symbols
    if re.search(r"[!@#$%^&*()\[\]{};:'\",.<>?/\\|`~+=_-]", text):
        return "ROT47"

    # Rule 5 — URL or slug
    if re.search(r"https?://|www\.", text, re.IGNORECASE):
        return "BASE62"

    # Rule 6 — looks like hex (only 0-9 and A-F)
    if re.fullmatch(r"[0-9a-fA-F]+", text) and len(text) % 2 == 0:
        return "BASE16"

    # Rule 7 — letters + digits mixed, long (over 80 chars)
    if re.fullmatch(r"[a-zA-Z0-9]+", text) and len(text) > 80:
        return "BASE85"

    # Rule 8 — letters + digits mixed, medium length
    if re.fullmatch(r"[a-zA-Z0-9]+", text) and len(text) > 20:
        return "ROT18"

    # Rule 9 — letters + digits mixed, short
    if re.fullmatch(r"[a-zA-Z0-9]+", text):
        return "ROT18"

    # Rule 10 — password / confidential type
    if "password" in msg_type:
        return "BASE64"

    # Default — normal readable sentence
    return "BASE64"


def explain(method):
    prompt = f"""
    Encoding method: {method}

    Write exactly 3 plain-text lines. No JSON, no bullets, no markdown symbols.

    Line 1 — starts with "Summary:" — one sentence: what this method does.
    Line 2 — starts with "Why this method:" — 2 sentences: why {method} is a good choice. Mention real advantages simply.
    Line 3 — starts with "Security Level:" — one of: Basic / Moderate / Strong, followed by a short reason.

    Keep language simple and friendly.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content