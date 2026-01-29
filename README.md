# poc-langchain

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.53.1-orange)](https://streamlit.io/)

Automatic Email & Calendar Assistant using **LangChain**, **Streamlit** and **Olloma** with ministral-3.

This assistant uses the **ministral-3** model via **Ollama** for natural language understanding and generation.

This project provides a conversational assistant capable of:

- Sending simulated emails.
- Creating simulated calendar events.
- Chatting naturally with the user when no action is required.

The interface uses **Streamlit** with chat bubbles (`st.chat_message`) and an interactive input field (`st.chat_input`).

---

## 📦 Installation

1. Install Olloma and ministral-3
https://docs.ollama.com/linux


2. Clone the project:

```bash
git clone https://github.com/your-username/poc-langchain.git
cd poc-langchain
cp .env.ex .env
poetry install
```

## 📦 Running the App
```bash
poetry shell
python main.py
---> http://localhost:8501/
```

## 📦 Mailhog

```bash
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
--> http://localhost:8025/
```