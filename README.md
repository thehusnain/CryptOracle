# CryptOracle

**CryptOracle** is a modern, AI-powered encoding and cryptographic assistant built with Python and Streamlit. It intelligently analyzes your messages and recommends the optimal encoding method based on the content, ensuring data is formatted securely and correctly.

## 🚀 Features

*   **AI-Powered Recommendations:** Utilizes the Groq API (LLaMA 3.3 70B) to analyze message content and suggest the best encoding method based on 11 deterministic rules.
*   **Comprehensive Encoding Suite:** Supports a wide array of both Base and ROT encodings:
    *   **Base Encodings:** Base16 (Hex), Base32, Base62, Base64, Base58 (Bitcoin alphabet), Base85, and Base91.
    *   **ROT Encodings:** ROT5, ROT13, ROT18, ROT47, and customizable ROT-N.
*   **Two-Way Operations:** Seamlessly encode your text or decode previously encoded messages directly from the interface.
*   **Clean, Modern UI:** Built with Streamlit, featuring a sleek dark-themed dashboard, responsive design, and integrated Bootstrap Icons.
*   **No Stored Data:** Processing happens entirely in-memory.

## 🛠️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/thehusnain/CryptOracle.git
    cd CryptOracle
    ```

2.  **Set up a virtual environment (recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install streamlit groq cryptography
    ```

4.  **Configure your API Key:**
    *   Create a `.streamlit` folder in the project root.
    *   Create a file named `secrets.toml` inside `.streamlit`.
    *   Add your Groq API key:
        ```toml
        GROQ_API_KEY = "your_actual_api_key_here"
        ```
    *(Note: `.streamlit/secrets.toml` is included in `.gitignore` to prevent accidental commits of your API key).*

5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 🧠 How the Recommendation Engine Works

When you submit a message, CryptOracle classifies it and applies rules to suggest the best encoding method. For example:

*   **Only digits:** Suggests `ROT5`.
*   **Short word/phrase:** Suggests `ROT13`.
*   **Contains symbols/punctuation:** Suggests `ROT47`.
*   **URLs or Slugs:** Suggests `BASE62` (URL safe).
*   **Passwords/Credentials:** Suggests `BASE64`.
*   **Large text blocks:** Suggests `BASE85` or `BASE91` for maximum compression.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/thehusnain/CryptOracle/issues) if you want to contribute.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
