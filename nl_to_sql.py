import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def nl_to_sql(user_question: str) -> str:
    prompt = f"""
    Convert this natural language question into an SQLite SQL query.
    Table: players
    Columns: name, club, goals, assists, matches, nationality
    Rules:
    - Use only this table and columns
    - Output SQL only (no text, no markdown)

    Question: {user_question}
    SQL:
    """

    res = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    sql = res.choices[0].message.content.strip()

    if "```" in sql:
        sql = sql.split("```")[1].replace("sql", "").strip()

    low = sql.lower()
    if not low.startswith("select ") or " from players" not in low:
        raise ValueError("Invalid SQL generated.")

    return sql
