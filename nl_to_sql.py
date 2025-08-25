import os
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def nl_to_sql(question: str) -> str:
    """
    Convert a natural language football question into SQL query.
    """
    prompt = f"""
    Convert this question into a valid SQLite SQL query.
    Table name is `players`.
    Only return SQL (no explanations, no markdown).
    If unsure, return: SELECT * FROM players LIMIT 10;

    Question: {question}
    """

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",  # ✅ supported Groq model
        messages=[
            {"role": "system", "content": "You are a SQL generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()
