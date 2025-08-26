import os
from groq import Groq

# ✅ Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def nl_to_sql(question: str) -> str:
    prompt = f"""
    Convert this question into a valid SQLite SQL query.
    Table name is `players`. 
    Column names are: name, position, club, market_value, age, primary_nationality,
    secondary_nationality, matches_played, goals, assists, yellow_cards, red_cards,
    substituted_in, substituted_out, second_yellow_cards, own_goals.
    
    Rules:
    - Always use lowercase column names exactly as given above.
    - Use WHERE name LIKE '%...%' instead of = for player names.
    - Only return SQL (no explanations, no markdown).
    - If unsure, return: SELECT * FROM players LIMIT 10;

    Question: {question}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        sql_query = response.choices[0].message.content.strip()

        # Ensure it starts with SELECT
        if not sql_query.lower().startswith("select"):
            return "SELECT * FROM players LIMIT 10;"

        return sql_query
    except Exception as e:
        print(f"⚠️ Groq API Error: {e}")
        return "SELECT * FROM players LIMIT 10;"
