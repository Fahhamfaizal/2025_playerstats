import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def nl_to_sql(question: str) -> str:
    prompt = f"""
    Convert this football question into a valid SQLite SQL query.
    Table name is `players`.
    
    Rules:
    - Column names are: "Name", "Position", "Club", "Market Value", "Age", "Primary Nationality", "Secondary Nationality",
      "Matches Played", "Goals", "Assists", "Yellow Cards", "Red Cards", "Substituted In", "Substituted Out",
      "Second Yellow Cards", "Own Goals".
    - Always wrap column names in double quotes.
    - For player names, always use: WHERE "Name" LIKE '%...%'
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

        if not sql_query.lower().startswith("select"):
            return 'SELECT * FROM players LIMIT 10;'

        return sql_query
    except Exception as e:
        print(f"⚠️ Groq API Error: {e}")
        return 'SELECT * FROM players LIMIT 10;'
