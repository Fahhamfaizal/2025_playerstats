from groq import Groq
import os
import streamlit as st

def nl_to_sql(question: str) -> str:
    """
    Always generate SQL using Groq LLM based on natural language input.
    """

    # Load key
    groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if not groq_api_key:
        st.error("❌ No Groq API key found.")
        st.stop()

    client = Groq(api_key=groq_api_key)

    prompt = (
        "Convert this question into a valid SQLite SQL query. "
        "Table name is `players`. "
        "Only return SQL (no explanations, no markdown). "
        "If unsure, return: SELECT * FROM players LIMIT 10; \n\n"
        f"Question: {question}"
    )

    # 👇 Print debug info (safe, no API key)
    st.write("🛠 Debug - Sending to Groq:")
    st.json({
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a SQL generator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    })

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
        st.error("❌ Error from Groq API. Please check the logs.")
        st.write("🛠 Debug - Exception type:", type(err).__name__)
        st.write("🛠 Debug - Exception details:", str(err))
        st.stop()

    if not sql_query.lower().startswith("select"):
        sql_query = "SELECT * FROM players LIMIT 10"

    return sql_query
