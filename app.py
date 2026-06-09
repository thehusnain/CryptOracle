# pyrefly: ignore [missing-import]
import streamlit as st

from ai_handler import classify_message, recommend_method, explain
from encryption_methods import (
    base16_encode, base16_decode,
    base32_encode, base32_decode,
    base64_encode, base64_decode,
    base62_encode, base62_decode,
    base58_encode, base58_decode,
    base85_encode, base85_decode,
    base91_encode, base91_decode,
    rot_n_encode,  rot_n_decode,
    rot13_encode,  rot13_decode,
    rot5_encode,   rot5_decode,
    rot18_encode,  rot18_decode,
    rot47_encode,  rot47_decode,
)

# All reversible methods 
ALL_METHODS = [
    "BASE16", "BASE32", "BASE64", "BASE62", "BASE58", "BASE85", "BASE91",
    "ROT13", "ROT5", "ROT18", "ROT47", "ROT-N",
]

# ROT-N uses a shift parameter — handled separately in the UI
DISPATCH = {
    "BASE16": (base16_encode, base16_decode),
    "BASE32": (base32_encode, base32_decode),
    "BASE64": (base64_encode, base64_decode),
    "BASE62": (base62_encode, base62_decode),
    "BASE58": (base58_encode, base58_decode),
    "BASE85": (base85_encode, base85_decode),
    "BASE91": (base91_encode, base91_decode),
    "ROT13":  (rot13_encode,  rot13_decode),
    "ROT5":   (rot5_encode,   rot5_decode),
    "ROT18":  (rot18_encode,  rot18_decode),
    "ROT47":  (rot47_encode,  rot47_decode),
}

# Page config
st.set_page_config(
    page_title="AI Encoding Assistant",
    page_icon="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/lock-fill.svg",
    layout="wide",
)

# Bootstrap Icons + minimal styling 
st.markdown(
    """
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"/>
    <style>
        .method-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 0.5rem 0.85rem;
            margin-bottom: 0.35rem;
            font-size: 0.86rem;
            color: #e2e8f0;
        }
        .method-card .tag { font-weight: 700; color: #38bdf8; }
        .oneway-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 0.5rem 0.85rem;
            margin-bottom: 0.35rem;
            font-size: 0.86rem;
            color: #64748b;
        }
        .oneway-card .tag { font-weight: 700; color: #94a3b8; }
        .section-label {
            font-size: 0.70rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #64748b;
            margin: 1rem 0 0.45rem 0;
        }
        .info-box {
            background: #0f172a;
            border-left: 3px solid #38bdf8;
            padding: 0.75rem 1rem;
            border-radius: 6px;
            color: #cbd5e1;
            font-size: 0.9rem;
            margin-top: 0.5rem;
            line-height: 1.6;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


#  SIDEBAR — Methods Dashboard
with st.sidebar:
    st.markdown(
        '<h3 style="margin:0 0 0.2rem 0;">'
        '<i class="bi bi-grid-fill"></i> Methods Dashboard'
        "</h3>",
        unsafe_allow_html=True,
    )

    st.caption("All supported encoding categories")

    # ── Base Encodings
    st.markdown(
        '<p class="section-label"><i class="bi bi-arrow-left-right"></i>'
        " Base Encodings — reversible</p>",
        unsafe_allow_html=True,
    )
    BASE_INFO = [
        ("BASE16", "bi-grid-1x2",      "Hex — color codes, MAC addresses"),
        ("BASE32", "bi-grid-3x3",      "Case-insensitive — URLs, file systems"),
        ("BASE64", "bi-braces",        "Industry standard — email, HTML images"),
        ("BASE62", "bi-link-45deg",    "No special chars — URL shorteners, IDs"),
        ("BASE58", "bi-currency-bitcoin", "Crypto alphabet — removes look-alike chars"),
        ("BASE85", "bi-file-earmark", "Compact — PDFs, PostScript, binary"),
        ("BASE91", "bi-lightning",     "Most compact ASCII encoding"),
    ]
    for name, icon, desc in BASE_INFO:
        st.markdown(
            f'<div class="method-card"><i class="bi {icon}"></i> '
            f'<span class="tag">{name}</span> — {desc}</div>',
            unsafe_allow_html=True,
        )

    #  ROT Encodings 
    st.markdown(
        '<p class="section-label"><i class="bi bi-arrow-repeat"></i>'
        " ROT Encodings — reversible</p>",
        unsafe_allow_html=True,
    )
    ROT_INFO = [
        ("ROT-N",  "bi-sliders",       "Custom letter shift (1–25)"),
        ("ROT13",  "bi-arrow-repeat",  "Half-alphabet — encode = decode"),
        ("ROT5",   "bi-123",           "Digits only, shift 5"),
        ("ROT18",  "bi-shuffle",       "ROT13 + ROT5 combined"),
        ("ROT47",  "bi-terminal",      "94 printable ASCII chars, shift 47"),
    ]
    for name, icon, desc in ROT_INFO:
        st.markdown(
            f'<div class="method-card"><i class="bi {icon}"></i> '
            f'<span class="tag">{name}</span> — {desc}</div>',
            unsafe_allow_html=True,
        )

    # ── One-Way (info only) 
    st.markdown(
        '<p class="section-label"><i class="bi bi-x-circle"></i>'
        " Hashing — one-way, not available</p>",
        unsafe_allow_html=True,
    )
    for name, desc in [("MD5","Legacy hash"),("SHA-256","Password hashing"),("SHA-512","High-security hashing")]:
        st.markdown(
            f'<div class="oneway-card"><i class="bi bi-dash-circle"></i> '
            f'<span class="tag">{name}</span> — {desc}</div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div class="info-box" style="margin-top:0.5rem;">'
        '<i class="bi bi-info-circle"></i> '
        "Hash functions are one-way operations. They cannot be reversed "
        "and are not available for encoding in this tool."
        "</div>",
        unsafe_allow_html=True,
    )


#  MAIN — Header

st.markdown(
    '<h1 style="margin-bottom:0.2rem;">'
    '<i class="bi bi-lock-fill"></i> AI Encoding Assistant'
    "</h1>",
    '<h2 style="margin-top:0.1rem; color:#64748b; font-weight:400;">'
    "Created and managed by Husnain and Usman"
    "</h2>",
    unsafe_allow_html=True,
)
st.caption("Enter your message — the AI will suggest the best encoding method.")
st.divider()

# Message input
message = st.text_area("Your Message", placeholder="Type or paste your message here...")


#  Analyze

if st.button("Analyze", type="primary"):
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Analyzing..."):
            msg_type = classify_message(message)
            method   = recommend_method(message, msg_type)
            # Guard: fall back if AI returns something not in our list
            if method not in ALL_METHODS:
                method = "BASE64"
            ai_text  = explain(method)

        # Parse the 3-line response
        parsed = {}
        for line in ai_text.splitlines():
            line = line.strip()
            if line.lower().startswith("summary:"):
                parsed["summary"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("why this method:"):
                parsed["why"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("security level:"):
                parsed["level"] = line.split(":", 1)[1].strip()

        st.session_state.msg_type = msg_type
        st.session_state.ai_method = method
        st.session_state.message   = message
        st.session_state.parsed    = parsed

# Show AI recommendation 
if "ai_method" in st.session_state:
    parsed = st.session_state.parsed
    ai_method = st.session_state.ai_method

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Message Type**\n\n{st.session_state.msg_type.capitalize()}")
    with col2:
        st.success(f"**AI Recommendation**\n\n{ai_method}")

    if parsed.get("summary"):
        st.markdown(
            f'<div class="info-box">'
            f'<i class="bi bi-chat-square-text"></i>&nbsp; {parsed["summary"]}'
            f"</div>",
            unsafe_allow_html=True,
        )

    if parsed.get("level"):
        lvl = parsed["level"]
        color = "#22c55e" if "strong" in lvl.lower() else "#f59e0b" if "moderate" in lvl.lower() else "#94a3b8"
        st.markdown(
            f'<div style="margin-top:0.5rem;">'
            f'<i class="bi bi-shield-check" style="color:{color};"></i>&nbsp;'
            f'<strong style="color:{color};">Security Level:</strong>&nbsp;'
            f'<span style="color:#cbd5e1;">{lvl}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

    if parsed.get("why"):
        with st.expander("Read More — Why this method is recommended"):
            st.markdown(
                f'<div class="info-box">'
                f"<strong>Why {ai_method}?</strong><br/><br/>{parsed['why']}"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.divider()

    #  STEP 2 — Encode
    st.markdown(
        '<h3 style="margin-bottom:0.4rem;">'
        '<i class="bi bi-key-fill"></i> Encode Message'
        "</h3>",
        unsafe_allow_html=True,
    )

    # Method selector — pre-filled with AI recommendation
    default_idx = ALL_METHODS.index(ai_method) if ai_method in ALL_METHODS else 2
    selected = st.selectbox("Choose encoding method", ALL_METHODS, index=default_idx)

    shift = 13  # default shown only for ROT-N
    if selected == "ROT-N":
        shift = st.slider("Shift value (N)", min_value=1, max_value=25, value=13)

    if st.button("Encode"):
        text = st.session_state.message
        try:
            if selected == "ROT-N":
                result = rot_n_encode(text, shift)
            else:
                encode_fn, _ = DISPATCH[selected]
                result = encode_fn(text)

            st.session_state.encoded_result = result
            st.session_state.encoded_method = selected
            st.session_state.encoded_shift  = shift

        except Exception as e:
            st.error(f"Encoding failed: {e}")

    if "encoded_result" in st.session_state:
        st.success("Encoded successfully")
        label = st.session_state.encoded_method
        if label == "ROT-N":
            label += f"  (shift = {st.session_state.encoded_shift})"
        st.markdown(f"**{label} Output**")
        st.code(st.session_state.encoded_result, language=None)


#  STEP 3 — Decode

st.divider()
st.markdown(
    '<h2 style="margin-bottom:0.4rem;">'
    '<i class="bi bi-unlock-fill"></i> Decode'
    "</h2>",
    unsafe_allow_html=True,
)
st.caption("Paste encoded text and select the method that was used.")

encoded_input = st.text_area("Encoded Text", key="decode_input")
decode_method = st.selectbox("Method used to encode", ALL_METHODS, key="decode_method_select")

decode_shift = 13
if decode_method == "ROT-N":
    decode_shift = st.slider("Shift value (N) used during encoding", 1, 25, 13, key="decode_shift")

if st.button("Decode"):
    if not encoded_input.strip():
        st.warning("Please paste the encoded text.")
    else:
        try:
            if decode_method == "ROT-N":
                result = rot_n_decode(encoded_input.strip(), decode_shift)
            else:
                _, decode_fn = DISPATCH[decode_method]
                result = decode_fn(encoded_input.strip())

            st.success("Decoded successfully")
            st.markdown("**Original Message**")
            st.code(result, language=None)

        except Exception:
            st.error(
                f"Could not decode. Make sure the text was encoded with {decode_method}."
            )
