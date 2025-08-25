import os
import streamlit as st
from groq import Groq

def nl_to_sql(question: str) -> str:
    groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error("❌ Groq API key not found. Set it in `.env` or `.streamlit/secrets.toml`.")
        st.stop()

    client = Groq(api_key=groq_api_key)

    prompt = (
        "Convert this question into a valid SQLite SQL query for the `players` table. "
        "Return only the SQL (no explanations, markdown, or backticks). "
        "If unsure, return: SELECT * FROM players LIMIT 10;\n\n"
        f"Question: {question}"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a SQL generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        sql_query = response.choices[0].message.content.strip()
    except Exception as err:
        st.error("❌ Error from Groq API. Check logs for details.")
        print("Groq API error:", repr(err))
        st.stop()

    if not sql_query.lower().startswith("select"):
        sql_query = "SELECT * FROM players LIMIT 10"

    return sql_query
