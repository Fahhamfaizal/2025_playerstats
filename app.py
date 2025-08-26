import os, sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from nl_to_sql import nl_to_sql
from create_db import create_database
from groq import Groq

DB_PATH = "football.db"

if not os.path.exists(DB_PATH):
    create_database()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ_API_KEY missing. Set it in your environment or Streamlit secrets.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="⚽ Football Data Explorer", layout="wide")
st.title("⚽ Football Data Explorer")

# User question
question = st.text_input("Ask a football question:")

if question:
    try:
        sql = nl_to_sql(question)
        st.code(sql, language="sql")

        con = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql, con)
        con.close()

        if df.empty:
            st.warning("No results found.")
        else:
            st.subheader("📋 Query Results")
            st.dataframe(df)

            # Auto visualization (only if numeric columns exist)
            num_cols = df.select_dtypes(include=["number"]).columns.tolist()
            if "name" in df.columns and len(num_cols) > 0:
                st.subheader("📊 Visualization")
                for col in num_cols:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    df_sorted = df.sort_values(col, ascending=False).head(10)
                    ax.bar(df_sorted["name"], df_sorted[col], color="skyblue", edgecolor="black")
                    ax.set_title(f"Player by {col.capitalize()}", fontsize=14, weight="bold")
                    ax.set_ylabel(col.capitalize())
                    ax.set_xticklabels(df_sorted["name"], rotation=45, ha="right")
                    st.pyplot(fig)

            # AI summary
            try:
                st.subheader("📝 Summary")
                prompt = f"Question: {question}\n\nData:\n{df.head(10).to_string(index=False)}\n\nWrite a short, clear summary."
                res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.2,
                )
                st.info(res.choices[0].message.content.strip())
            except Exception as e:
                st.warning(f"Summary failed: {e}")

    except Exception as e:
        st.error(f"SQL execution error: {e}")


