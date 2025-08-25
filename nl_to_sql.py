from groq import Groq
import os
import streamlit as st

def nl_to_sql(question: str) -> str:
    """
    Always generate SQL using Groq LLM based on natural language input.
    """

    groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

    if not groq_api_key:
        st.error("❌ Groq API key not found. Please set it in `.env` (local) or `.streamlit/secrets.toml` (cloud).")
        st.stop()

    client = Groq(api_key=groq_api_key)

    prompt = f"""
    Convert this question into a valid SQLite SQL query.
    - The table name is `players`
    - Only return SQL (no explanations, no markdown, no backticks)
    - If unsure, return: SELECT * FROM players LIMIT 10;

    Question: {question}
    """

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    # ✅ Correct field access for Groq
    sql_query = response.choices[0].message.content.strip()

    if not sql_query.lower().startswith("select"):
        sql_query = "SELECT * FROM players LIMIT 10"

    return sql_query
