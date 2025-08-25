import os
import streamlit as st
from groq import Groq, BadRequestError

# ✅ Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def nl_to_sql(question: str) -> str:
    prompt = f"""
    Convert this question into a valid SQLite SQL query.
    Table name is `players`.
    Only return SQL (no explanations, no markdown).
    If unsure, return: SELECT * FROM players LIMIT 10;

    Question: {question}
    """

    try:
        # 🚀 Debug: Show outgoing request
        print("🚀 Sending request to Groq API...")
        print("Model:", "llama-3.1-70b-versatile")
        print("Prompt:", prompt)

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # ✅ Supported model
            messages=[
                {"role": "system", "content": "You are a SQL generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        sql = response.choices[0].message.content.strip()
        print("✅ SQL Generated:", sql)  # Debug log
        return sql

    except BadRequestError as e:
        # ❌ Groq API specific error
        print("❌ Groq BadRequestError:", e)  # Logs full details
        st.error(f"⚠️ Groq API Error: {str(e)}")
        return "SELECT * FROM players LIMIT 10;"  # fallback query

    except Exception as e:
        # ❌ Unexpected errors
        print("❌ Unexpected Error:", e)
        st.error(f"⚠️ Unexpected Error: {str(e)}")
        return "SELECT * FROM players LIMIT 10;"  # fallback query
