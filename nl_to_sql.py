import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ Missing GROQ_API_KEY. Set it as env var or Streamlit secret.")

client = Groq(api_key=api_key)

def nl_to_sql(user_question: str) -> str:
    prompt = f"""
    Convert this into a valid SQLite query.
    Table: players
    Columns:
    name, position, club, market_value, age, primary_nationality, secondary_nationality,
    matches_played, goals, assists, yellow_cards, red_cards,
    substituted_in, substituted_out, second_yellow_cards, own_goals.

    Rules:
    - Use lowercase column names exactly as above
    - For player lookups use: WHERE name LIKE '%<player>%'
    - Return SQL only, no markdown
    - If unsure: SELECT * FROM players LIMIT 10;

    Question: {user_question}
    """

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    sql = res.choices[0].message.content.strip()
    if not sql.lower().startswith("select"):
        sql = "SELECT * FROM players LIMIT 10;"
    return sql
