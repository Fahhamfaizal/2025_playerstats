import os
import streamlit as st
from groq import Groq
import json

def nl_to_sql(question: str) -> str:
    groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error("API key missing. Add it in `.env` or `.streamlit/secrets.toml`.")
        st.stop()
    client = Groq(api_key=groq_api_key)

    prompt = (
        "Convert the following question into a valid SQLite SQL query targeting the `players` table. "
        "Return only the SQL (no explanations, no markdown). If unsure, return:\nSELECT * FROM players LIMIT 10;\n\n"
        f"Question: {question}"
    )

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a SQL generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        sql_query = response.choices[0].message.content.strip()
    except Exception as err:
        # Log error details for debugging (not shown to the user)
        st.error("Error from Groq API. Please check your logs.")
        print("Groq API error:", repr(err))
        st.stop()

    if not sql_query.lower().startswith("select"):
        sql_query = "SELECT * FROM players LIMIT 10"

    return sql_query
