
import streamlit as st
from groq import Groq


MODEL_NAME = "openai/gpt-oss-20b"


def get_groq_client():

    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key or not api_key.strip():
        raise RuntimeError("Groq API key is missing.")

    return Groq(api_key=api_key)


def test_groq_connection():

    client = get_groq_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Groq connection successful!"
            }
        ],
        max_completion_tokens=100,
    )

    return response.choices[0].message.content
